from rest_framework import serializers

from user.models import RegistrationApplication


class RegistrationApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["email", "name", "file", "description"]


class RegistrationApplicationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["id", "email", "name", "file", "description", "status", "created_at"]


class RegistrationApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["status"]
