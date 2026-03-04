from django.urls import path
from . import views

urlpatterns=[
    path('tutor/', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/lesson/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('tutor/lesson/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),
]
