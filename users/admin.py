from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Notification

# Регистрируем нашу кастомную модель пользователя
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Notification)
