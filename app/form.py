from django import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class  MyPasswordResetFrom(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
