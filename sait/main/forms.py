from .models import Application
from django.forms import ModelForm, TextInput, DateTimeInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ["type", "name", "date"]

        widgets = {
            "type": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название этапа"
            }),
            "name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Имя"
            }),
            "date": DateTimeInput(attrs={
                "class": "form-control",
                "placeholder": "Дата заявки"
            }),
        }

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Логин'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'autocomplete': 'off', 'placeholder': 'Почта'})
    )
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        return self.cleaned_data.get("password2")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data