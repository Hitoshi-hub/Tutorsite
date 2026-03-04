from django.urls import path
from . import views # Импортируем функции-обработчики (Views)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:pk>/', views.profile_view, name='profile_detail'),
    path('cabinet/', views.profile_view, name='cabinet'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='notification_read'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
