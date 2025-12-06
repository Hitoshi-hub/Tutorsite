from django.shortcuts import render
from django.http import HttpResponse

# Заглушка для register_view
def register_view(request):
    # Эта функция пока ничего не делает, но ее достаточно, чтобы Django прошел проверку
    return HttpResponse("Страница регистрации (ЗАГЛУШКА)")

# Заглушка для login_view
def login_view(request):
    return HttpResponse("Страница входа (ЗАГЛУШКА)")

# Заглушка для profile_view
def profile_view(request):
    return HttpResponse("Страница для профиля (ЗАГЛУШКА)")
