from django.urls import path, include
from rest_framework.routers import DefaultRouter

from band.views import (
    BandImageListCreateView,
    BandImageRetrieveDestroyView,
    CommentsListCreateDestroyView,
    BandViewSet,
)

app_name = "band"

router = DefaultRouter()
router.register("", BandViewSet, basename="bands")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:band_id>/images/",
        BandImageListCreateView.as_view(),
        name="band-images-list-create",
    ),
    path(
        "<int:band_id>/images/<int:image_id>/",
        BandImageRetrieveDestroyView.as_view(),
        name="band-image-detail",
    ),
    path(
        "<int:band_id>/comments/",
        CommentsListCreateDestroyView.as_view(),
        name="comments-list-create",
    ),
    path(
        "<int:user_id>/comments/<int:pk>/",
        CommentsListCreateDestroyView.as_view(),
        name="comments-destroy",
    ),
]
