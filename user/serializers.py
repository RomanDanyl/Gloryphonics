from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.files.uploadedfile import UploadedFile
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from user.models import (
    RegistrationApplication,
    UserImage,
    Album,
    Follower,
    SocialLinks,
    RegistrationToken,
)


MAX_FILE_SIZE_MB = 100


class CompleteRegistrationSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_token(self, value: str) -> str:
        try:
            token_obj = RegistrationToken.objects.select_related("application").get(
                token=value
            )
        except RegistrationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

        if not token_obj.is_valid():
            raise serializers.ValidationError("Token has expired.")

        self.context["token_obj"] = token_obj

        return value

    def validate(self, attrs):
        token_obj = self.context.get("token_obj")
        if not token_obj:
            raise serializers.ValidationError("Token validation failed.")

        attrs["application"] = token_obj.application
        attrs["token_obj"] = token_obj
        return attrs


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

        max_size = MAX_FILE_SIZE_MB * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(f'File size must be under {MAX_FILE_SIZE_MB}MB')

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


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    return_url = serializers.URLField()

    def validate_email(self, value):
        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value


class PasswordResetRequestResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(min_length=5, write_only=True)

    def validate_password(self, value) -> Optional[str]:
        if len(value) < 5:
            raise serializers.ValidationError(
                "Password must be at least 5 characters long"
            )
        return value

    def validate(self, attrs) -> Optional[dict]:
        try:
            uid = urlsafe_base64_decode(attrs["uidb64"]).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError("Invalid UID or user")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        attrs["user"] = user
        return attrs


class PasswordResetConfirmResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


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
