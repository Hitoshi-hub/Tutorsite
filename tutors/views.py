from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TutorProfile
from .forms import TutorProfileForm 
from .models import TutorProfile

def tutor_detail(request, pk):
    # Пытаемся найти репетитора по ID (pk), если нет — показываем 404
    tutor = get_object_or_404(TutorProfile, pk=pk)
    
    return render(request, 'tutors/tutor_detail.html', {'tutor': tutor})

def tutor_list(request):
    # 1. Сначала ПОЛУЧАЕМ данные
    tutors = TutorProfile.objects.all()
    
    # 2. Обрабатываем поиск (если он есть)
    query = request.GET.get('search')
    if query:
        tutors = tutors.filter(subjects__name__icontains=query).distinct()
    
    # 3. ОБЯЗАТЕЛЬНО возвращаем результат в самом конце!
    # Проверь, чтобы этот return НЕ стоял внутри блока 'if query'
    return render(request, 'tutors/tutor_list.html', {'tutors': tutors})

@login_required # Только залогиненные могут стать репетиторами
def become_tutor(request):
    # Если у пользователя уже есть профиль репетитора, просто отправляем его туда
    if hasattr(request.user, 'tutor_profile'):
        return redirect('tutor_detail', pk=request.user.tutor_profile.pk)

    if request.method == 'POST':
        form = TutorProfileForm(request.POST)
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