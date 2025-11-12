import uuid

from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import models
from django.utils import timezone

from band.models import Band
from user.utils import (
    avatar_upload_path,
    registration_file_upload_path,
)


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "user", "User"
        MEMBER = "member", "Member"
        MANAGER = "manager", "Manager"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        choices=RoleChoices.choices, default=RoleChoices.USER, max_length=10
    )
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    country = models.CharField(max_length=100)
    band = models.ForeignKey(
        Band, on_delete=models.SET_NULL, null=True, blank=True, related_name="members"
    )

    def __str__(self):
        return self.get_full_name() or self.username


class RegistrationToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    application = models.OneToOneField(
        "RegistrationApplication", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self) -> bool:
        return timezone.now() < self.expires_at


class RegistrationApplication(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        APPROVED = "Approved"
        REJECTED = "Rejected"

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    file = models.FileField(upload_to=registration_file_upload_path, max_length=355)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=15
    )

    def __str__(self) -> str:
        return f"Application from {self.name}, email - {self.email}"
