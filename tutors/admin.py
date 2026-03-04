from django.contrib import admin
from .models import TutorProfile, Subject, Review, TutorStudentLink, StudentGroup

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # Автозаполнение слага из имени

admin.site.register(TutorProfile)
admin.site.register(Review)
admin.site.register(TutorStudentLink)
admin.site.register(StudentGroup)
