from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissionsOrAnonReadOnly,
)

from band.models import BandImage, Band, Comment
from user.models import User
from user.permissions import IsOwnerOrAdminOrReadOnly
from band.serializers import (
    UserImageCreateSerializer,
    BandImageReadSerializer,
    CommentSerializer,
    BandListSerializer,
)


class BandImageListCreateView(generics.ListCreateAPIView):
    serializer_class = UserImageCreateSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    def get_queryset(self):
        band_id = self.kwargs["band_id"]
        return BandImage.objects.get_or_404(band_id=band_id)

    def perform_create(self, serializer):
        band_id = self.kwargs["band_id"]
        band = get_object_or_404(Band, pk=band_id)
        serializer.save(band=band)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BandImageReadSerializer
        return UserImageCreateSerializer


class BandImageRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = BandImageReadSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        band_id = self.kwargs["band_id"]
        return BandImage.objects.filter(band_id=band_id)

    def perform_create(self, serializer):
        band_id = self.kwargs["band_id"]
        band = get_object_or_404(Band, pk=band_id)
        serializer.save(group=band)


class CommentsListCreateDestroyView(
    generics.ListCreateAPIView, generics.DestroyAPIView
):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Comment.objects.filter(group__id=user_id).select_related("group")

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, pk=user_id)
        serializer.save(group=user)


class BandViewSet(viewsets.ModelViewSet):
    serializer_class = BandListSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Band.objects.all().prefetch_related(
        "genres",
        "images",
        "videos",
        "members",
        "albums",
        "followers",
        "social_links",
        "comments",
    )

    # def get_queryset(self):
    #     return self.queryset.filter(is_superuser=False, is_staff=False)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BandListSerializer
        return BandListSerializer
