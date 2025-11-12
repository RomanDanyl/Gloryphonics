from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    RegistrationApplicationViewSet,
    CreateUserView,
    ManageUserView,
    UserListRetrieveUpdateView,
    CompleteRegistrationView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

app_name = "user"

router = DefaultRouter()
router.register("applications", RegistrationApplicationViewSet, basename="applications")
router.register("", UserListRetrieveUpdateView, basename="users")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("", include(router.urls)),
    path("me/", ManageUserView.as_view(), name="manage"),
    path(
        "complete-registration/",
        CompleteRegistrationView.as_view(),
        name="complete-registration",
    ),
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
