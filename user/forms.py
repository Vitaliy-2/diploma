from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Адрес электронной почты"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))


    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


    # Валидация поля email
    def clean_email(self):
        email = self.cleaned_data["email"]
        # Проверяет, есть ли такой же email в базе. exists() - возвращает bool
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Данный адрес электронной почты уже зарегистрирован в системе")
        # Если проверка прошла, пропускаем email дальше
        return email