from rest_framework import serializers

from user.models import RegistrationApplication


class RegistrationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationApplication
        fields = ["email", "name", "file", "description"]
