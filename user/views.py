from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from user.emails import send_reject_email, send_approve_email, send_create_email
from user.models import RegistrationApplication, UserImage, User
from user.permissions import IsOwnerOrAdminOrReadOnly
from user.serializers import (
    RegistrationApplicationCreateSerializer,
    RegistrationApplicationReadSerializer,
    RegistrationApplicationUpdateSerializer,
    CreateUserSerializer,
    UserSerializer,
    UserImageCreateSerializer,
    UserImageReadSerializer,
)


class RegistrationApplicationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = RegistrationApplication.objects.all()
    serializer_class = RegistrationApplicationCreateSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]

        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "create":
            return RegistrationApplicationCreateSerializer
        if self.action == "partial_update":
            return RegistrationApplicationUpdateSerializer
        return RegistrationApplicationReadSerializer

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        old_status = instance.status

        response = super().partial_update(request, *args, **kwargs)

        instance.refresh_from_db(fields=["status"])
        new_status = instance.status

        if old_status != new_status:
            if new_status == "Approved":
                send_approve_email(instance)
            elif new_status == "Rejected":
                send_reject_email(instance)

        return response

    def perform_create(
        self, serializer: RegistrationApplicationCreateSerializer
    ) -> None:
        application = serializer.save()
        send_create_email(application)


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> get_user_model():
        return self.request.user


class UserImageListCreateView(generics.ListCreateAPIView):
    serializer_class = UserImageCreateSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return UserImage.objects.filter(user_id=user_id).select_related("user")

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, pk=user_id)
        serializer.save(user=user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserImageReadSerializer
        return UserImageCreateSerializer


class UserImageRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = UserImageReadSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return UserImage.objects.filter(user_id=user_id)


class UserListRetrieveView(viewsets.ReadOnlyModelViewSet):
    pass
