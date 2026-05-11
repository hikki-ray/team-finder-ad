from django.contrib.auth.models import AbstractUser
from django.db import models

from core.utils import generate_avatar
from users.constants import (
    MAX_ABOUT_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_SURNAME_LENGTH,
)
from users.managers import UserManager


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
