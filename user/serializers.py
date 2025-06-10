from rest_framework import serializers

from user.models import RegistrationApplication


class RegistrationApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["email", "name", "file", "description"]

    def validate_file(self, value):
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
