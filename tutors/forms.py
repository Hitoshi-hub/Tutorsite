from django import forms
from django.utils.text import slugify
from .models import TutorProfile, Review, Subject

class TutorProfileForm(forms.ModelForm):
    custom_subject = forms.CharField(
        required=False,
        max_length=100,
        label='Свой предмет',
        help_text='Если нужного предмета нет в списке, введите его здесь.',
        widget=forms.TextInput(attrs={'placeholder': 'Например: Астрономия'}),
    )

    class Meta:
        model = TutorProfile
        # Поля, которые пользователь будет заполнять сам
        fields = ['avatar', 'subjects', 'bio', 'hourly_rate', 'experience_years', 'city']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(), # Красивый выбор галочками
            'bio': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Расскажите о своей методике...'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город или онлайн'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.order_by('name')

    def clean_custom_subject(self):
        value = (self.cleaned_data.get('custom_subject') or '').strip()
        return value

    def save(self, commit=True):
        profile = super().save(commit=commit)
        custom_subject_name = self.cleaned_data.get('custom_subject')
        if custom_subject_name:
            subject = Subject.objects.filter(name__iexact=custom_subject_name).first()
            if not subject:
                base_slug = slugify(custom_subject_name) or 'subject'
                slug = base_slug
                i = 2
                while Subject.objects.filter(slug=slug).exists():
                    slug = f'{base_slug}-{i}'
                    i += 1
                subject = Subject.objects.create(name=custom_subject_name, slug=slug)
            profile.subjects.add(subject)
        return profile

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Поделитесь впечатлениями...'}),
        }
