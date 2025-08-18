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
)


class UserManager(DjangoUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields: Any) -> "User":
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str, **extra_fields: Dict[str, Any]
    ) -> "User":
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields: Dict[str, Any]
    ) -> "User":
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "User"
        MANAGER = "Manager"
        ADMIN = "Admin"

    username = None
    email = models.EmailField(_("email address"), unique=True)
    country = models.CharField(max_length=100)
    avatar = models.ImageField(
        upload_to=avatar_upload_path, max_length=355, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)
    role = models.CharField(
        choices=RoleChoices.choices, default=RoleChoices.USER, max_length=10
    )
    genres = models.ManyToManyField("Genre", related_name="groups")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_image_upload_path)

    def __str__(self) -> str:
        return f"Image from user {self.user.username}"


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
    name = models.CharField(max_length=255)


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
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    spotify = models.URLField(blank=True, null=True)
    youtube_music = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Social links for {self.user.username}"


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="members")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to=member_photo_upload_path)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
