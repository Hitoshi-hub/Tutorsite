from django.contrib import admin
from .models import TutorProfile, Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # Автозаполнение слага из имени

admin.site.register(TutorProfile)