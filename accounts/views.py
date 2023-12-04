

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm
from app.models import Dish
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseNotFound
import csv
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User not found. Please try again.')
    return render(request, 'login.html')
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RussianUserCreationForm(UserCreationForm):
    # Переопределение полей и текстовых меток формы
    username = forms.CharField(
        label="Имя пользователя",
        strip=False,
        help_text="Обязательное поле. Максимум 150 символов. Можно использовать только буквы, цифры и символы @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Ваш пароль не должен содержать персональную информацию и должен быть не менее 8 символов."
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Введите пароль еще раз для подтверждения."
    )

    class Meta(UserCreationForm.Meta):
        # Переопределение метаданных формы
        fields = UserCreationForm.Meta.fields


def register_view(request):
    if request.method == 'POST':
        form = RussianUserCreationForm(request.POST)
        if form.is_valid():
            # Действия при успешной регистрации
            form.save()
            return redirect('home')
    else:
        form = RussianUserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def home(request):
    return render(request, 'home.html')


