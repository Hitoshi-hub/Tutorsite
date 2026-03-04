from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Conversation, Message
from tutors.models import TutorProfile
from tutors.models import TutorStudentLink


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(
        Q(student=request.user) | Q(tutor=request.user)
    ).select_related('student', 'tutor')

    return render(request, 'chat/thread_list.html', {
        'conversations': conversations,
    })


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.filter(Q(student=request.user) | Q(tutor=request.user)),
        pk=pk,
    )
    

    # Все входящие сообщения в этом диалоге считаем прочитанными.
    conversation.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    if request.method == 'POST':
        action = request.POST.get('action', 'send_message')

        if action == 'send_message':
            body = request.POST.get('body', '').strip()
            if body:
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    body=body,
                    is_read=False,
                )
                conversation.updated_at = timezone.now()
                conversation.save(update_fields=['updated_at'])

        elif action == 'request_enrollment' and request.user == conversation.student:
            pending_exists = Message.objects.filter(
                conversation=conversation,
                kind='enrollment_request',
                enrollment_student=request.user,
                enrollment_status='pending',
            ).exists()
            if not pending_exists:
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    body='Хочу записаться к вам на занятия.',
                    kind='enrollment_request',
                    enrollment_student=request.user,
                    is_read=False,
                )
                conversation.updated_at = timezone.now()
                conversation.save(update_fields=['updated_at'])

        elif action == 'accept_enrollment' and request.user == conversation.tutor:
            message_id = request.POST.get('message_id')
            enrollment_message = get_object_or_404(
                Message,
                pk=message_id,
                conversation=conversation,
                kind='enrollment_request',
                enrollment_status='pending',
            )

            tutor_profile = get_object_or_404(TutorProfile, user=conversation.tutor)
            TutorStudentLink.objects.get_or_create(
                tutor=tutor_profile,
                student=enrollment_message.enrollment_student,
            )
            enrollment_message.enrollment_status = 'accepted'
            enrollment_message.save(update_fields=['enrollment_status'])

        return redirect('chat_detail', pk=pk)

    return render(request, 'chat/thread_detail.html', {
        'conversation': conversation,
        'messages': conversation.messages.select_related('sender', 'enrollment_student'),
    })


@login_required
def start_chat(request, tutor_id):
    tutor_profile = get_object_or_404(TutorProfile, pk=tutor_id)
    tutor_user = tutor_profile.user

    if tutor_user == request.user:
        return redirect('tutor_detail', pk=tutor_id)

    conversation, _ = Conversation.objects.get_or_create(
        student=request.user,
        tutor=tutor_user,
    )

    return redirect('chat_detail', pk=conversation.pk)
