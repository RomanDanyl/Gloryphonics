from django.contrib.auth.models import AbstractUser
from django.db import models

from user.utills import (
    avatar_upload_path,
    user_image_upload_path,
    registration_file_upload_path,
    album_cover_upload_path,
)


class User(AbstractUser):
    country = models.CharField(max_length=100)
    avatar = models.ImageField(
        upload_to=avatar_upload_path, max_length=355, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_image_upload_path)

    def __str__(self) -> str:
        return f"Image from user {self.user.username}"


class RegistrationApplication(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        APPROVED = "Approved"
        REJECTED = "Rejected"

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=registration_file_upload_path, max_length=355)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=15
    )

    def __str__(self) -> str:
        return f"Application from {self.name}, email - {self.email}"


class Album(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to=album_cover_upload_path)

    def __str__(self):
        return self.title
