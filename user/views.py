from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from user.emails import send_reject_email, send_approve_email
from user.models import RegistrationApplication
from user.serializers import (
    RegistrationApplicationCreateSerializer,
    RegistrationApplicationReadSerializer,
    RegistrationApplicationUpdateSerializer,
    CreateUserSerializer,
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
        send_approve_email(application)


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
