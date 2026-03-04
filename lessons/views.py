from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import StudentGroupForm, TutorLessonForm
from .models import Lesson
from tutors.models import StudentGroup, TutorStudentLink
from users.models import Notification
from chat.models import Conversation, Message


def _lesson_target_students(lesson):
    if lesson.group_id:
        return list(lesson.group.members.all())
    if lesson.student_id:
        return [lesson.student]
    return []


def _lesson_event_text(lesson, action):
    subject = lesson.subject.name if lesson.subject else 'Занятие'
    time_text = timezone.localtime(lesson.start_time).strftime('%d.%m.%Y %H:%M')
    if lesson.group_id:
        target = f"группа «{lesson.group.name}»"
    else:
        target = lesson.student.username

    if action == 'created':
        title = 'Назначено занятие'
        body = f"{subject}, {time_text}, {target}"
    elif action == 'updated':
        title = 'Изменено занятие'
        body = f"{subject}, {time_text}, {target}"
    else:
        title = 'Занятие удалено'
        body = f"{subject}, {time_text}, {target}"
    return title, body


def _notify_students_about_lesson(lesson, action):
    students = _lesson_target_students(lesson)
    title, body = _lesson_event_text(lesson, action)
    tutor_user = lesson.tutor.user

    for student in students:
        Notification.objects.create(
            user=student,
            kind=f'lesson_{action}',
            title=title,
            body=body,
            link=reverse('profile'),
        )
        conversation, _ = Conversation.objects.get_or_create(student=student, tutor=tutor_user)
        Message.objects.create(
            conversation=conversation,
            sender=tutor_user,
            body=f"Уведомление: {title.lower()} — {body}",
            kind='text',
            is_read=False,
        )


@login_required
def tutor_dashboard(request):
    tutor_profile = getattr(request.user, 'tutor_profile', None)
    if not tutor_profile:
        return redirect('profile')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_group':
            group_form = StudentGroupForm(request.POST, tutor_profile=tutor_profile)
            lesson_form = TutorLessonForm(tutor_profile=tutor_profile)
            if group_form.is_valid():
                group_form.save()
                return redirect('tutor_dashboard')
        elif action == 'create_lesson':
            group_form = StudentGroupForm(tutor_profile=tutor_profile)
            lesson_form = TutorLessonForm(request.POST, tutor_profile=tutor_profile)
            if lesson_form.is_valid():
                lesson = lesson_form.save()
                _notify_students_about_lesson(lesson, action='created')
                return redirect('tutor_dashboard')
        else:
            group_form = StudentGroupForm(tutor_profile=tutor_profile)
            lesson_form = TutorLessonForm(tutor_profile=tutor_profile)
    else:
        group_form = StudentGroupForm(tutor_profile=tutor_profile)
        lesson_form = TutorLessonForm(tutor_profile=tutor_profile)

    attached_students = TutorStudentLink.objects.filter(tutor=tutor_profile).select_related('student')
    groups = StudentGroup.objects.filter(tutor=tutor_profile).prefetch_related('members', 'subject')
    lessons = (
        Lesson.objects.filter(tutor=tutor_profile)
        .select_related('student', 'group', 'subject')
        .order_by('start_time')
    )

    return render(
        request,
        'lessons/tutor_dashboard.html',
        {
            'group_form': group_form,
            'lesson_form': lesson_form,
            'attached_students': attached_students,
            'groups': groups,
            'lessons': lessons[:20],
        },
    )


@login_required
def lesson_edit(request, lesson_id):
    tutor_profile = getattr(request.user, 'tutor_profile', None)
    if not tutor_profile:
        return redirect('profile')

    lesson = get_object_or_404(
        Lesson.objects.select_related('group', 'student', 'subject', 'tutor__user').prefetch_related('group__members'),
        pk=lesson_id,
        tutor=tutor_profile,
    )

    if request.method == 'POST':
        form = TutorLessonForm(request.POST, instance=lesson, tutor_profile=tutor_profile)
        if form.is_valid():
            updated_lesson = form.save()
            _notify_students_about_lesson(updated_lesson, action='updated')
            return redirect('tutor_dashboard')
    else:
        form = TutorLessonForm(instance=lesson, tutor_profile=tutor_profile)

    return render(
        request,
        'lessons/lesson_edit.html',
        {
            'form': form,
            'lesson': lesson,
        },
    )


@login_required
def lesson_delete(request, lesson_id):
    tutor_profile = getattr(request.user, 'tutor_profile', None)
    if not tutor_profile:
        return redirect('profile')

    lesson = get_object_or_404(
        Lesson.objects.select_related('group', 'student', 'subject', 'tutor__user').prefetch_related('group__members'),
        pk=lesson_id,
        tutor=tutor_profile,
    )
    if request.method == 'POST':
        _notify_students_about_lesson(lesson, action='deleted')
        lesson.delete()
    return redirect('tutor_dashboard')
