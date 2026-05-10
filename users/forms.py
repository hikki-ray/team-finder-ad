import re

from django import forms
from django.contrib.auth import authenticate

from core.constants import GITHUB_URL_PATTERN, MSG_GITHUB_INVALID
from users.constants import (
    MSG_EMAIL_TAKEN,
    MSG_GITHUB_TAKEN,
    MSG_INVALID_VALUES,
    MSG_PHONE_INVALID,
    MSG_PHONE_PATTERN,
    MSG_PHONE_TAKEN,
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
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not phone:
            return phone

        if not re.match(MSG_PHONE_PATTERN, phone):
            raise forms.ValidationError(MSG_PHONE_INVALID)

        normalized = "+7" + phone[1:] if phone.startswith("8") else phone
        if self._field_taken("phone", normalized):
            raise forms.ValidationError(MSG_PHONE_TAKEN)

        return normalized

    def clean_github_url(self):
        url = (self.cleaned_data.get("github_url") or "").strip()
        if not url:
            return url

        if not re.match(GITHUB_URL_PATTERN, url):
            raise forms.ValidationError(MSG_GITHUB_INVALID)

        normalized = url.rstrip("/")
        if self._field_taken("github_url", normalized):
            raise forms.ValidationError(MSG_GITHUB_TAKEN)

        return normalized

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if self._field_taken("email", email):
            raise forms.ValidationError(MSG_EMAIL_TAKEN)
        return email

    def _field_taken(self, field, value):
        queryset = User.objects.filter(**{field: value})
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        return queryset.exists()
