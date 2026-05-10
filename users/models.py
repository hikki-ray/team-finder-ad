from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.utils import generate_avatar
from users.constants import (
    MAX_ABOUT_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_SURNAME_LENGTH,
    MSG_EMAIL_REQUIRED,
    MSG_SUPERUSER_STAFF,
    MSG_SUPERUSER_SUPERUSER,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(MSG_EMAIL_REQUIRED)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(MSG_SUPERUSER_STAFF)
        if not extra_fields.get("is_superuser"):
            raise ValueError(MSG_SUPERUSER_SUPERUSER)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField("Имя", max_length=MAX_NAME_LENGTH)
    surname = models.CharField("Фамилия", max_length=MAX_SURNAME_LENGTH)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    phone = models.CharField("Телефон", max_length=MAX_PHONE_LENGTH, blank=True)
    github_url = models.URLField("GitHub", blank=True)
    about = models.TextField("О себе", blank=True, max_length=MAX_ABOUT_LENGTH)
    email = models.EmailField("Email", unique=True)
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранное",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.name} {self.surname}".strip() or self.email

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)
