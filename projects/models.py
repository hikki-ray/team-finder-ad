from django.conf import settings
from django.db import models
from django.urls import reverse

from projects.constants import MAX_PROJECT_NAME_LENGTH, MAX_PROJECT_STATUS_LEGTH


class ProjectState(models.TextChoices):
    ACTIVE = "open", "Открыт"
    INACTIVE = "closed", "Закрыт"


class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
    )
    name = models.CharField("Название", max_length=MAX_PROJECT_NAME_LENGTH)
    description = models.TextField("Описание", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    status = models.CharField(
        "Статус",
        max_length=MAX_PROJECT_STATUS_LEGTH,
        choices=ProjectState.choices,
        default=ProjectState.ACTIVE,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"pk": self.pk})
