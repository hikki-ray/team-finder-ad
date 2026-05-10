from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "name", "surname", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active", "is_superuser", "date_joined")
    search_fields = ("email", "name", "surname", "phone")
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined")
    fieldsets = (
        ("Учётные данные", {"fields": ("email", "password")}),
        ("Профиль", {"fields": ("name", "surname", "avatar", "phone", "github_url", "about")}),
        (
            "Права",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2"),
            },
        ),
    )
