from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import Application

COURSE_CHOICES = [
    ('algorithms', 'Основы алгоритмизации и программирования'),
    ('web_design', 'Основы веб-дизайна'),
    ('databases', 'Основы проектирования баз данных'),
]

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    full_name = forms.CharField(label='ФИО', max_length=150)
    phone = forms.CharField(label='Телефон', max_length=16)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z0-9]{6,}$', username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры (минимум 6 символов)')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[А-Яа-яЁё\s]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы')
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX')
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    course_name = forms.ChoiceField(choices=COURSE_CHOICES)

    class Meta:
        model = Application
        fields = ['course_name', 'start_date', 'payment_method']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }