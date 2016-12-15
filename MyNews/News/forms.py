from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин', }),
        max_length=30, min_length=5, required=True, label='Логин'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Иван', }),
        max_length=30, required=True, label='Имя'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Иванов', }),
        max_length=30, required=True, label='Фамилия'
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login@gmail.com', }),
        required=True, max_length=254, label='E-mail'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*****'}),
        min_length=8, label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*****'}),
        min_length=8, label=u'Повторите пароль'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('Such user already exists')
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError('Пароли не совпадают!')

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        return authenticate(username=u.username, password=password)


class SigninForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Логин', }
        ),
        max_length=30,
        label='Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '*******', }
        ),
        label='Пароль'
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('Такого пользователя не существует!')
        else:
            raise forms.ValidationError('Не правильный логин или пароль')
