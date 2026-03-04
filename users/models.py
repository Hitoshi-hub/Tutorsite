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


class Notification(models.Model):
    KIND_CHOICES = [
        ('lesson_created', 'Назначено занятие'),
        ('lesson_updated', 'Изменено занятие'),
        ('lesson_deleted', 'Удалено занятие'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='notifications')
    kind = models.CharField(max_length=30, choices=KIND_CHOICES)
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"
