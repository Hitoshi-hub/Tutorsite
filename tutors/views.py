from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from decimal import Decimal, InvalidOperation
from .models import TutorProfile, Subject
from .forms import TutorProfileForm, ReviewForm


def _safe_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return None


def tutor_detail(request, pk):
    # Пытаемся найти репетитора по ID (pk), если нет — показываем 404
    tutor = get_object_or_404(TutorProfile, pk=pk)
    
    reviews = tutor.reviews.select_related('author').all().order_by('-created_at')
    rating_stats = reviews.aggregate(avg=Avg('rating'))
    avg_rating = rating_stats['avg'] or 0
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') # Или просто запретить отправку в шаблоне
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tutor = tutor
            review.author = request.user
            review.save()
            return redirect('tutor_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'tutors/tutor_detail.html', {
        'tutor': tutor,
        'reviews': reviews,
        'form': form,
        'avg_rating': avg_rating,
        'reviews_count': reviews.count(),
    })


def tutor_list(request):
    # 1. Сначала ПОЛУЧАЕМ данные
    tutors = (
        TutorProfile.objects.select_related('user')
        .prefetch_related('subjects')
        .annotate(avg_rating=Avg('reviews__rating'), reviews_count=Count('reviews'))
    )
    
    # 2. Обрабатываем поиск (если он есть)
    query = request.GET.get('q') or request.GET.get('search')
    subject_id = request.GET.get('subject')
    city = request.GET.get('city')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    min_exp = request.GET.get('min_exp')

    if query:
        tutors = tutors.filter(
            Q(user__username__icontains=query)
            | Q(bio__icontains=query)
            | Q(subjects__name__icontains=query)
            | Q(city__icontains=query)
        )

    if subject_id and str(subject_id).isdigit():
        tutors = tutors.filter(subjects__id=int(subject_id))

    if city:
        tutors = tutors.filter(city__icontains=city)

    min_rate_value = _safe_decimal(min_rate)
    max_rate_value = _safe_decimal(max_rate)

    if min_rate_value is not None:
        tutors = tutors.filter(hourly_rate__gte=min_rate_value)

    if max_rate_value is not None:
        tutors = tutors.filter(hourly_rate__lte=max_rate_value)

    if min_exp and str(min_exp).isdigit():
        tutors = tutors.filter(experience_years__gte=int(min_exp))

    tutors = tutors.distinct()
    
    # 3. ОБЯЗАТЕЛЬНО возвращаем результат в самом конце!
    # Проверь, чтобы этот return НЕ стоял внутри блока 'if query'
    return render(request, 'tutors/tutor_list.html', {
        'tutors': tutors,
        'subjects': Subject.objects.all().order_by('name'),
        'query': query or '',
        'city': city or '',
        'min_rate': min_rate or '',
        'max_rate': max_rate or '',
        'min_exp': min_exp or '',
        'subject_id': subject_id or '',
    })

@login_required # Только залогиненные могут стать репетиторами
def become_tutor(request):
    # Если у пользователя уже есть профиль репетитора, просто отправляем его туда
    if hasattr(request.user, 'tutor_profile'):
        return redirect('tutor_detail', pk=request.user.tutor_profile.pk)

    if request.method == 'POST':
        form = TutorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user # Привязываем профиль к текущему юзеру
            profile.save()
            form.save_m2m() # Важно для сохранения предметов (ManyToMany)
            
            # Помечаем пользователя как репетитора
            request.user.is_tutor = True
            request.user.save()
        return redirect('tutor_list') 
    else:
        form = TutorProfileForm()

    # 2. Отправляем их в HTML-шаблон
    return render(request, 'tutors/become_tutor.html', {'form': form})

@login_required
def edit_tutor_profile(request):
    # Берем профиль именно текущего юзера
    profile = get_object_or_404(TutorProfile, user=request.user)
    
    if request.method == 'POST':
        # instance=profile говорит Django обновить старую запись, а не создавать новую
        form = TutorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') # Возвращаемся в кабинет
    else:
        form = TutorProfileForm(instance=profile)
    
    return render(request, 'tutors/become_tutor.html', {'form': form, 'edit': True})
