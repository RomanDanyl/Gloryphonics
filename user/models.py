import os
import pathlib
import uuid
from typing import Callable, Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


def path_factory(folder_name: str) -> Callable[[Any, str], str]:
    def path(instance, filename: str) -> str:
        username = (
            instance.user.username
            if hasattr(instance, "user") and instance.user
            else (instance.username if hasattr(instance, "username") else "unknown")
        )
        filename = f"{slugify(username)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
        return os.path.join("upload", folder_name, filename)

    return path


class User(AbstractUser):
    country = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=path_factory("avatars"), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to=lambda instance, filename: path_factory(
            f"images/{instance.user.id if instance.user else 'unknown'}"
        )(instance, filename)
    )

    def __str__(self) -> str:
        return f"Image from user {self.user.username}"


class RegistrationApplication(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=path_factory("files"))
    description = models.TextField()

    def __str__(self) -> str:
        return f"Application from {self.name}, email - {self.email}"
