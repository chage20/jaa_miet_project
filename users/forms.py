from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'city', 'password1', 'password2')
        # Явно задаём id и data-validate, чтобы ваш registration.js работал без правок
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'data-validate': 'username', 'id': 'username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'data-validate': 'name', 'id': 'name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'data-validate': 'name', 'id': 'lastname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'data-validate': 'email', 'id': 'email'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'data-validate': 'city', 'id': 'city'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'data-validate': 'password', 'id': 'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'data-validate': 'password_confirm', 'id': 'password_confirm'}),
        }