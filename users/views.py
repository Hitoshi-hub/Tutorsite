from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.utils import timezone
from .forms import StudentRegistrationForm
from lessons.models import Lesson
from tutors.models import TutorProfile, TutorStudentLink
from .models import Notification


def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Сразу логиним пользователя после регистрации
            return redirect('home') # Редирект на главную страницу
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # Или куда тебе нужно после входа
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    # Пытаемся получить профиль репетитора, если он есть
    tutor_profile = getattr(request.user, 'tutor_profile', None)

    lesson_query = Q(student=request.user) | Q(group__members=request.user)
    if tutor_profile:
        lesson_query = Q(tutor=tutor_profile) | lesson_query

    now = timezone.now()
    lessons = (
        Lesson.objects.filter(lesson_query)
        .select_related('tutor__user', 'student', 'subject', 'group')
        .prefetch_related('group__members')
        .distinct()
        .order_by('start_time')
    )

    upcoming_lessons = lessons.filter(start_time__gte=now)[:12]
    past_lessons = lessons.filter(start_time__lt=now)[:6]

    my_tutors = (
        TutorProfile.objects.filter(
            Q(student_links__student=request.user)
            | Q(lessons__student=request.user)
            | Q(lessons__group__members=request.user)
        )
        .select_related('user')
        .distinct()
    )

    my_students = []
    if tutor_profile:
        my_students = (
            TutorStudentLink.objects.filter(tutor=tutor_profile)
            .select_related('student')
            .values_list('student__username', flat=True)
            .distinct()
        )

    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_end = (month_start + timedelta(days=32)).replace(day=1)
    calendar_lessons = lessons.filter(start_time__gte=month_start, start_time__lt=month_end)

    lessons_payload = [
        {
            'title': (
                f"{lesson.subject.name if lesson.subject else 'Занятие'} · "
                f"{lesson.tutor.user.username if request.user != lesson.tutor.user else (lesson.group.name if lesson.group else lesson.student.username)}"
            ),
            'start': lesson.start_time.isoformat(),
            'status': lesson.status,
        }
        for lesson in calendar_lessons
    ]

    context = {
        'user': request.user,
        'tutor_profile': tutor_profile,
        'upcoming_lessons': upcoming_lessons,
        'past_lessons': past_lessons,
        'my_tutors': my_tutors,
        'my_students': my_students,
        'lessons_payload': lessons_payload,
    }
    return render(request, 'users/profile.html', context)


@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'users/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    if notification.link:
        return redirect(notification.link)
    return redirect('notifications')
