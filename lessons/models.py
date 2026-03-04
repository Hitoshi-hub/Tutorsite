from django.db import models
from django.db.models import Q
from django.conf import settings
from tutors.models import TutorProfile, Subject, StudentGroup


class Lesson(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    ]

    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='lessons')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True,
    )
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(student__isnull=False) & Q(group__isnull=True))
                    | (Q(student__isnull=True) & Q(group__isnull=False))
                ),
                name='lesson_has_exactly_one_target',
            )
        ]

    def __str__(self):
        subject = self.subject.name if self.subject else 'Занятие'
        if self.group:
            target = f"группа {self.group.name}"
        else:
            target = self.student.username if self.student else 'ученик'
        return f"{subject} · {self.tutor.user.username} -> {target}"
