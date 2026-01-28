from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login 
from .forms import StudentRegistrationForm


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

# Заглушка для login_view
def login_view(request):
    return HttpResponse("Страница входа (ЗАГЛУШКА)")

# Заглушка для profile_view
def profile_view(request):
    return HttpResponse("Страница для профиля (ЗАГЛУШКА)")
