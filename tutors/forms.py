from django import forms
from .models import TutorProfile

class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        # Поля, которые пользователь будет заполнять сам
        fields = ['subjects', 'bio', 'hourly_rate', 'experience_years']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(), # Красивый выбор галочками
            'bio': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Расскажите о своей методике...'}),
        }