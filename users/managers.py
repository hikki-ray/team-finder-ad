from django.contrib.auth.base_user import BaseUserManager

from users.constants import (
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
