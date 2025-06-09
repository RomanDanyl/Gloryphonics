from django.urls import path
from user.views import create_registration_application


app_name = "user"

urlpatterns = [
    path(
        "applications/create/",
        create_registration_application,
        name="application-create",
    ),
]
