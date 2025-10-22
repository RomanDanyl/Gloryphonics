from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    RegistrationApplicationViewSet,
    CreateUserView,
    ManageUserView,
    UserImageListCreateView,
    UserImageRetrieveDestroyView,
    UserListRetrieveUpdateView,
    CompleteRegistrationView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    CommentsListCreateDestroyView,
)

app_name = "user"

router = DefaultRouter()
router.register("applications", RegistrationApplicationViewSet, basename="applications")
router.register("artists", UserListRetrieveUpdateView, basename="users")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("", include(router.urls)),
    path("me/", ManageUserView.as_view(), name="manage"),
    path(
        "<int:user_id>/images/",
        UserImageListCreateView.as_view(),
        name="user-images-list-create",
    ),
    path(
        "<int:user_id>/images/<int:image_id>/",
        UserImageRetrieveDestroyView.as_view(),
        name="user-image-detail",
    ),
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
    path(
        "<int:user_id>/comments/",
        CommentsListCreateDestroyView.as_view(),
        name="comments-list-create",
    ),
    path(
        "<int:user_id>/comments/<int:pk>/",
        CommentsListCreateDestroyView.as_view(),
        name="comments-destroy",
    ),
]
