from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gloryphonics import settings
from user.serializers import RegistrationApplicationSerializer


@api_view(["POST"])
def create_registration_application(request: HttpRequest) -> Response:
    serializer = RegistrationApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    application = serializer.save()

    subject = "New registration application"
    message = (
        f"Email: {application.email}\n"
        f"Name: {application.name}\n"
        f"File: {application.file.url if application.file else '---'}\n"
        f"Description: {application.description}"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_201_CREATED)
