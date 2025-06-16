from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    RegistrationApplicationViewSet,
    CreateUserView,
    ManageUserView,
    UserImageListCreateView,
    UserImageRetrieveDestroyView,
)

app_name = "user"

router = DefaultRouter()
router.register("applications", RegistrationApplicationViewSet, basename="applications")

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
        "<int:user_id>/images/<int:pk>/",
        UserImageRetrieveDestroyView.as_view(),
        name="user-image-detail",
    ),
]
