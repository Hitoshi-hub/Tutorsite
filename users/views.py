from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import StudentRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


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
    
    context = {
        'user': request.user,
        'tutor_profile': tutor_profile,
    }
    return render(request, 'users/profile.html', context)