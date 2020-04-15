from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Imię', widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(label='Powtórz hasło',
                                widget=forms.PasswordInput(attrs={'placeholder': "Powtórz hasło"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(LoginForm, self).get_form(form_class)
        form.fields['username'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
        form.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Hasło'})
        return form
