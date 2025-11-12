from django.urls import path, include
from rest_framework.routers import DefaultRouter

from band.views import (
    BandImageListCreateView,
    BandImageRetrieveDestroyView,
    CommentsListCreateDestroyView,
    BandViewSet,
)

app_name = "user"

router = DefaultRouter()
router.register("", BandViewSet, basename="bands")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:band_id>/images/",
        BandImageListCreateView.as_view(),
        name="user-images-list-create",
    ),
    path(
        "<int:band_id>/images/<int:image_id>/",
        BandImageRetrieveDestroyView.as_view(),
        name="user-image-detail",
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
