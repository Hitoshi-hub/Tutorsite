from django.urls import path
from . import views # Импортируем функции-обработчики (Views)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:pk>/', views.profile_view, name='profile_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]