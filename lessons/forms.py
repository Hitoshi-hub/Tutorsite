from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime

from .models import Lesson
from tutors.models import StudentGroup, TutorStudentLink


class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = ['name', 'subject', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Математика 8 класс'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'members': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, tutor_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tutor_profile = tutor_profile
        linked_students = TutorStudentLink.objects.filter(tutor=tutor_profile).select_related('student')
        student_ids = [item.student_id for item in linked_students]
        self.fields['members'].queryset = get_user_model().objects.filter(pk__in=student_ids).order_by('username')
        self.fields['subject'].queryset = tutor_profile.subjects.all().order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tutor = self.tutor_profile
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class TutorLessonForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    start_clock = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'HH:MM',
                'inputmode': 'numeric',
                'pattern': '^([01]\\d|2[0-3]):[0-5]\\d$',
            },
            format='%H:%M',
        ),
        input_formats=['%H:%M'],
    )

    class Meta:
        model = Lesson
        fields = ['subject', 'student', 'group', 'duration_minutes', 'status']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 30, 'step': 15}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, tutor_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tutor_profile = tutor_profile
        linked_students = TutorStudentLink.objects.filter(tutor=tutor_profile).select_related('student')
        student_ids = [item.student_id for item in linked_students]
        self.fields['student'].queryset = get_user_model().objects.filter(pk__in=student_ids).order_by('username')
        self.fields['student'].required = False
        self.fields['group'].queryset = StudentGroup.objects.filter(tutor=tutor_profile).order_by('name')
        self.fields['group'].required = False
        self.fields['subject'].queryset = tutor_profile.subjects.all().order_by('name')
        self.fields['subject'].required = False
        self.fields['start_clock'].help_text = '24-часовой формат'

        if self.instance and self.instance.pk and self.instance.start_time:
            local_start = timezone.localtime(self.instance.start_time)
            self.fields['start_date'].initial = local_start.date()
            self.fields['start_clock'].initial = local_start.strftime('%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        group = cleaned_data.get('group')
        if bool(student) == bool(group):
            raise forms.ValidationError('Нужно выбрать либо одного ученика, либо группу.')

        start_date = cleaned_data.get('start_date')
        start_clock = cleaned_data.get('start_clock')
        if start_date and start_clock:
            start_naive = datetime.combine(start_date, start_clock)
            cleaned_data['start_time'] = timezone.make_aware(start_naive, timezone.get_current_timezone())
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tutor = self.tutor_profile
        instance.start_time = self.cleaned_data['start_time']
        if commit:
            instance.save()
        return instance
