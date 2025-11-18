import random
import string

from django.db import models
from django.utils.text import slugify

from user.utils import (
    album_cover_upload_path,
    cover_image_upload_path,
    band_image_upload_path,
)


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

    def get_slug(self) -> str:
        """
        Generate a slug from the band's name and append two random alphanumeric characters.
        Example: "Red Hot Chili Peppers" -> "red-hot-chili-peppers-x9"
        """
        rand_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=2)
        )
        return f"{slugify(self.name)}-{rand_suffix}"


class BandImage(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=band_image_upload_path)

    def __str__(self) -> str:
        return f"Band's {self.band.name} image #{self.id}"


class BandVideo(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="videos")
    playlist = models.CharField(max_length=255)

    def __str__(self):
        return f"Band's {self.band.name} video playlist #{self.id}"


class Album(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="albums")
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
        Band,
        related_name="followers",
        blank=True,
    )

    def __str__(self):
        return f"{self.name} <{self.email}>"


class SocialLinks(models.Model):
    band = models.OneToOneField(
        Band, on_delete=models.CASCADE, related_name="social_links"
    )
    facebook = models.URLField(blank=True, null=True, unique=True)
    instagram = models.URLField(blank=True, null=True, unique=True)
    youtube = models.URLField(blank=True, null=True, unique=True)
    spotify = models.URLField(blank=True, null=True, unique=True)
    youtube_music = models.URLField(blank=True, null=True, unique=True)

    def __str__(self):
        return f"Social links for {self.band.name}"


class Comment(models.Model):
    group = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255)

    def __str__(self):
        return self.text
