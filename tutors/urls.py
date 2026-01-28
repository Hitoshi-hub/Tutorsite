from django.urls import path
from . import views

urlpatterns=[
    path('', views.tutor_list, name='tutor_list'),
    path('<int:pk>/', views.tutor_detail, name='tutor_detail'),
    path('become/', views.become_tutor, name='become_tutor'),
]
