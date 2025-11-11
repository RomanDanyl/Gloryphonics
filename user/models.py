import uuid
from typing import Dict, Any

from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from user.utils import (
    avatar_upload_path,
    user_image_upload_path,
    registration_file_upload_path,
    album_cover_upload_path,
    member_photo_upload_path,
    cover_image_upload_path,
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
        "Band", on_delete=models.SET_NULL, null=True, related_name="members"
    )

    def __str__(self):
        return self.get_full_name() or self.username


class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField("Genre", related_name="bands")
    cover_image = models.ImageField(
        upload_to=cover_image_upload_path, blank=True, null=True
    )

    def __str__(self):
        return self.name


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_image_upload_path)

    def __str__(self) -> str:
        return f"Image from user {self.user.username}"


class UserVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    playlist = models.URLField()


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


class Album(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to=album_cover_upload_path)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Follower(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    followed_artists = models.ManyToManyField(
        User,
        related_name="followers",
        blank=True,
    )

    def __str__(self):
        return f"{self.name} <{self.email}>"


class SocialLinks(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="social_links"
    )
    facebook = models.URLField(blank=True, null=True, unique=True)
    instagram = models.URLField(blank=True, null=True, unique=True)
    youtube = models.URLField(blank=True, null=True, unique=True)
    spotify = models.URLField(blank=True, null=True, unique=True)
    youtube_music = models.URLField(blank=True, null=True, unique=True)

    def __str__(self):
        return f"Social links for {self.user.username}"


class Comment(models.Model):
    group = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255)

    def __str__(self):
        return self.text
