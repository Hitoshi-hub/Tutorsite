from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    # Мы наследуемся от стандартной формы, но указываем нашу модель
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email') # Поля, которые увидит пользователь

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True  # По умолчанию регистрируем как ученика
        if commit:
            user.save()
        return user


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',)
