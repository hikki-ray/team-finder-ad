from django import forms
from django.contrib.auth import authenticate

from core.utils import clean_github_url, clean_phone
from users.constants import (
    MSG_GITHUB_TAKEN,
    MSG_INVALID_VALUES,
)
from users.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(request=self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(MSG_INVALID_VALUES)

        return self.cleaned_data

    def get_user(self):
        return self.user


class ProfileUpdateForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "https://github.com/<user>"}),
    )

    class Meta:
        model = User
        fields = ("avatar", "name", "surname", "about", "phone", "github_url")

    def clean_phone(self):
        return clean_phone(
            self.cleaned_data.get("phone"),
            model=User,
            instance_pk=self.instance.pk
        )

    def clean_github_url(self):
        return clean_github_url(
            self.cleaned_data.get("github_url"),
            model=User,
            instance_pk=self.instance.pk,
            error_msg=MSG_GITHUB_TAKEN
        )
