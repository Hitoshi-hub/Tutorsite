from django.db import models
from users.models import CustomUser
from django.conf import settings



class Subject(models.Model):
    # Предметы, которые можно преподавать (например, "Математика", "Английский").
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True) # Поле для создания читаемого url

    def __str__(self):
        return self.name

class TutorProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tutor_profile'
    )
    
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Фото профиля")
    
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


class TutorStudentLink(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='student_links')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor_links')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tutor', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tutor.user.username} -> {self.student.username}"


class StudentGroup(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='student_groups')
    name = models.CharField(max_length=120)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tutor', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.tutor.user.username})"


class Review(models.Model):
    # Связываем отзыв с репетитором
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='reviews')
    # Связываем отзыв с автором (учеником)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    text = models.TextField(verbose_name="Ваш отзыв")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.author.username} для {self.tutor.user.username}"
