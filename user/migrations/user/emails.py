from django.core.mail import send_mail

from gloryphonics import settings
from user.models import RegistrationApplication


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


def send_approve_email(application: RegistrationApplication) -> None:
    print(f"Sending approve email for {application.name}")


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
