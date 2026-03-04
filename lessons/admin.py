from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'tutor', 'student', 'group', 'subject', 'start_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('tutor__user__username', 'student__username', 'group__name')
