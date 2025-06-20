from typing import Optional

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from user.models import RegistrationApplication, UserImage


class RegistrationApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["email", "name", "file", "description"]

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
        fields = ["id", "email", "name", "file", "description", "status", "created_at"]


class RegistrationApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["status"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "first_name",
            "last_name",
            "avatar",
            "country",
            "description",
            "slogan",
        )
        read_only_fields = ("is_staff",)

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


class CreateUserSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
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
