from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__email", "owner__name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    filter_horizontal = ("participants",)
    autocomplete_fields = ("owner",)
    fieldsets = (
        ("Основное", {"fields": ("name", "description", "owner")}),
        ("Ссылки и статус", {"fields": ("github_url", "status")}),
        ("Команда", {"fields": ("participants",)}),
        ("Дата", {"fields": ("created_at",)}),
    )
