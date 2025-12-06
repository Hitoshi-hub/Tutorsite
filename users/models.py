from django.db import models
from django.contrib.auth.models import AbstractUser

# Расширение стандартной модели пользователя Django
class CustomUser(AbstractUser):
    # Дополнительные поля для идентификации типа пользователя
    is_tutor = models.BooleanField(
        default=False, 
        verbose_name='Является ли пользователь репетитором'
    )
    is_student = models.BooleanField(
        default=False, 
        verbose_name='Является ли пользователь учеником'
    )
    
    # Поле для аватара важно чтобы поле можно было оставить пустым, а таблица могла хранить пустое значение (blanc для первого, null для второго)
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.username