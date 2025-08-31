import os
import pathlib
import uuid
from typing import Callable, Any

from django.utils.text import slugify


def avatar_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a file path for uploading a user's avatar.

    The filename will be constructed from a slugified username and a unique UUID,
    preserving the original file extension.

    Args:
        instance: The model instance containing the user data.
        filename: The original filename of the uploaded file.

    Returns:
        A string representing the path where the avatar will be stored.
    """
    username = instance.username if instance.username else "unknown"
    filename = f"{slugify(username)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return os.path.join("upload", "avatars", filename)


def user_image_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a file path for uploading a user-related image.

    The filename will be constructed from the user's slugified username and a unique UUID,
    preserving the original file extension. The path includes the user's ID as a directory.

    Args:
        instance: The model instance containing the user image data.
        filename: The original filename of the uploaded file.

    Returns:
        A string representing the path where the image will be stored.
    """
    user_id = instance.user.id if instance.user else "unknown"
    username = instance.user.username if instance.user else "unknown"
    filename = f"{slugify(username)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return os.path.join("upload", "images", str(user_id), filename)


def registration_file_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a file path for uploading a registration-related file.

    The filename will be constructed from a slugified name attribute of the instance and a unique UUID,
    preserving the original file extension.

    Args:
        instance: The model instance containing the registration data.
        filename: The original filename of the uploaded file.

    Returns:
        A string representing the path where the registration file will be stored.
    """
    username = instance.name if instance.name else "unknown"
    filename = f"{slugify(username)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return os.path.join("upload", "files", filename)


def album_cover_upload_path(instance: Any, filename: str) -> str:
    """
    Generate upload path for album cover images.

    Files will be saved to: albums/<artist_id>/<slugified-title>-<uuid>.<ext>
    """
    artist_id = instance.artist.id if instance.artist else "unknown"
    title_slug = slugify(instance.title) or "untitled"
    ext = pathlib.Path(filename).suffix
    new_filename = f"{title_slug}-{uuid.uuid4()}{ext}"
    return os.path.join("upload", "albums", str(artist_id), new_filename)


def member_photo_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a file path for member's photo.

    The filename will be constructed from a slugified first_name
    and last_name attribute of the instance and a unique UUID,
    preserving the original file extension.

    Args:
        instance: The model instance containing the member data.
        filename: The original filename of the uploaded file.

    Returns:
        A string representing the path where the registration file will be stored.
    """
    name = (
        instance.first_name
        if instance.first_name
        else "unknown" + instance.last_name if instance.last_name else "unknown"
    )
    filename = f"{slugify(name)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return os.path.join("upload", "members_photos", filename)


def cover_image_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a file path for uploading a user's cover image.

    The filename will be constructed from a slugified user email and a unique UUID,
    preserving the original file extension.

    Args:
        instance: The model instance containing the user data.
        filename: The original filename of the uploaded file.

    Returns:
        A string representing the path where the avatar will be stored.
    """
    user_email = instance.email if instance.email else "unknown"
    filename = f"{slugify(user_email)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return os.path.join("upload", "cover_images", filename)


def user_video_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a file path for uploading a user-related video.

    The filename will be constructed from the user's slugified user email and a unique UUID,
    preserving the original file extension. The path includes the user's ID as a directory.

    Args:
        instance: The model instance containing the user image data.
        filename: The original filename of the uploaded file.

    Returns:
        A string representing the path where the image will be stored.
    """
    user_id = instance.user.id if instance.user else "unknown"
    email = instance.user.email if instance.user else "unknown"
    filename = f"{slugify(email)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return os.path.join("upload", "videos", str(user_id), filename)
