from typing import Optional

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from user.models import (
    RegistrationApplication,
    UserImage,
    Album,
    Follower,
    SocialLinks,
    RegistrationToken,
)


class CompleteRegistrationSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_token(self, value: str) -> Optional[str]:
        try:
            token = RegistrationToken.objects.select_related("application").get(
                token=value
            )
        except RegistrationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

        if not token.is_valid():
            raise serializers.ValidationError("Token has expired.")

        return value


class RegistrationApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["email", "name", "country", "file", "description"]

    def validate_file(self, value: UploadedFile) -> Optional[UploadedFile]:
        """
        Validates that the uploaded file is either an audio or video file.
        """
        if not value:
            return value

        content_type = value.content_type

        allowed_main_types = ["audio", "video"]

        if not any(
            content_type.startswith(main_type) for main_type in allowed_main_types
        ):
            raise serializers.ValidationError(
                "Unsupported file type. Only audio and video files are allowed."
            )

        return value


class RegistrationApplicationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = [
            "id",
            "email",
            "name",
            "country",
            "file",
            "description",
            "status",
            "created_at",
        ]


class RegistrationApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["status"]


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = (
            "id",
            "title",
            "release_date",
            "cover_image",
        )


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ("id", "name", "email")


class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = ("facebook", "instagram", "youtube", "spotify", "youtube_music")


class UserListSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
    social_links = SocialLinksSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "avatar",
            "country",
            "description",
            "slogan",
            "social_links",
            "albums",
            "followers",
        )

    def create(self, validated_data: dict) -> get_user_model():
        """Create a new users with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(
        self, instance: get_user_model(), validated_data: dict
    ) -> get_user_model():
        """Update a users, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class CreateUserSerializer(UserListSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "country",
            "avatar",
            "description",
            "slogan",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }


class UserImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ["image"]


class UserImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ["id", "user", "image"]


class UserRetrieveSerializer(UserListSerializer):
    images = UserImageReadSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "avatar",
            "country",
            "description",
            "slogan",
            "social_links",
            "albums",
            "followers",
            "images",
        )
