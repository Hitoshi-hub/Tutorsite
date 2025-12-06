from django.db import models
from users.models import CustomUser

class Subject(models.Model):
    # Предметы, которые можно преподавать (например, "Математика", "Английский").
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True) # Поле для создания читаемого url

    def __str__(self):
        return self.name

class TutorProfile(models.Model):
    # Подробная информация о репетиторе.
    
    # Связь с моделью пользователя (один к одному)
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='tutor_profile'
    )
    
    # Основная информация
    bio = models.TextField(
        verbose_name='Краткая биография и описание', 
        max_length=1000
    )
    experience_years = models.PositiveSmallIntegerField(
        default=0, 
        verbose_name='Опыт преподавания (лет)'
    )
    
    # Предметы (отношение "многие ко многим")
    subjects = models.ManyToManyField(
        Subject, 
        related_name='tutors', 
        verbose_name='Преподаваемые предметы'
    )
    
    # Цена
    hourly_rate = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name='Цена за час (валюта)'
    )
    
    # Местоположение (можно использовать для фильтрации)
    city = models.CharField(max_length=100, blank=True)
    
    # Автоматическое обновление
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль репетитора: {self.user.username}"
