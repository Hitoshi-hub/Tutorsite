"""
URL configuration for tutorsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Общая/главная страница
    path('accounts/', include('users.urls')), # users
    path('tutors/', include('tutors.urls')), # tutors
    path('lessons/', include('lessons.urls')), # lessons
    # path('reviews/', include('reviews.urls')), # можно включить в tutors
    # path('payments/', include('payments.urls')), # можно включить в lessons
    path('chat/', include('chat.urls')), # chat
]
