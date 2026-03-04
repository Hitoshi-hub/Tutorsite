from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list, name='chat_list'),
    path('start/<int:tutor_id>/', views.start_chat, name='chat_start'),
    path('<int:pk>/', views.conversation_detail, name='chat_detail'),
]
