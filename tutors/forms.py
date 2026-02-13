from django import forms
from .models import TutorProfile, Review

class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        # Поля, которые пользователь будет заполнять сам
        fields = ['subjects', 'bio', 'hourly_rate', 'experience_years']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(), # Красивый выбор галочками
            'bio': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Расскажите о своей методике...'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Поделитесь впечатлениями...'}),
        }