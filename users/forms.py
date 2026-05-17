from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    # Мы наследуемся от стандартной формы, но указываем нашу модель
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email') # Поля, которые увидит пользователь

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].help_text = (
            'Минимум 8 символов. Пароль не должен быть слишком простым, '
            'состоять только из цифр или быть похожим на ваши личные данные.'
        )
        self.fields['password2'].help_text = 'Введите тот же пароль еще раз для подтверждения.'
        self.fields['password2'].error_messages['required'] = 'Подтвердите пароль.'
        self.error_messages['password_mismatch'] = 'Пароли не совпадают.'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            return password1
        try:
            validate_password(password1, self.instance)
        except ValidationError as exc:
            raise ValidationError([
                f'Пароль не подходит: {message}' for message in exc.messages
            ])
        return password1

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
