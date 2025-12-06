from django.urls import path
from . import views # Импортируем функции-обработчики (Views)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:pk>/', views.profile_view, name='profile_detail'),
    # мб в будущем добавим что-то ещё
]