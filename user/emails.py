from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from gloryphonics import settings
from user.models import RegistrationApplication, RegistrationToken


def send_reject_email(application: RegistrationApplication) -> None:
    subject = "Your registration has been rejected"
    message = (
        f"Dear {application.name},\n"
        f"We regret to inform you that your registration application has been rejected.\n"
        f"If you have any questions, please don't hesitate to contact us.\n\n"
        f"Sincerely,\n"
        f"The Gloryphonic Team\n"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [application.email],
        fail_silently=False,
    )


def send_approve_email(application: RegistrationApplication, token: str) -> None:
    link = f"https://frontend-site.com/complete-registration/?token={token}"

    send_mail(
        subject="Your application has been approved",
        message=(
            f"Congratulations!\n\n"
            f"Your application has been approved. "
            f"Please complete your registration by visiting the following link:\n\n{link}\n\n"
            f"The link is valid for one week"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[application.email],
    )


def send_create_email(application: RegistrationApplication) -> None:
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


def send_password_reset_email(user: get_user_model(), reset_url: str) -> None:
    send_mail(
        subject="Password Reset Request",
        message=f"Click the link below to reset your password:\n{reset_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
