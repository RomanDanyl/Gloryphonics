from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, generics, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.emails import (
    send_reject_email,
    send_approve_email,
    send_create_email,
    send_password_reset_email,
)
from user.models import RegistrationApplication, UserImage, User, RegistrationToken
from user.permissions import IsOwnerOrAdminOrReadOnly
from user.serializers import (
    RegistrationApplicationCreateSerializer,
    RegistrationApplicationReadSerializer,
    RegistrationApplicationUpdateSerializer,
    CreateUserSerializer,
    UserListSerializer,
    UserImageCreateSerializer,
    UserImageReadSerializer,
    UserRetrieveSerializer,
    CompleteRegistrationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetRequestResponseSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetConfirmResponseSerializer,
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
            if new_status == RegistrationApplication.StatusChoices.APPROVED:
                token = RegistrationToken.objects.create(
                    application=instance, expires_at=timezone.now() + timedelta(days=7)
                )
                send_approve_email(instance, token.token)
            elif new_status == RegistrationApplication.StatusChoices.REJECTED:
                send_reject_email(instance)

        return response

    def perform_create(
        self, serializer: RegistrationApplicationCreateSerializer
    ) -> None:
        application = serializer.save()
        send_create_email(application)


class CompleteRegistrationView(APIView):
    @extend_schema(
        request=CompleteRegistrationSerializer,
        responses={200: CreateUserSerializer},
    )
    def post(self, request):
        serializer = CompleteRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]
        application = serializer.validated_data["application"]
        token_obj = serializer.validated_data["token_obj"]

        user = get_user_model().objects.create_user(
            email=application.email,
            description=application.description,
            country=application.country,
            password=password,
        )

        token_obj.delete()

        return Response(CreateUserSerializer(user).data, status=status.HTTP_201_CREATED)


class PasswordResetRequestView(APIView):
    """
    View to handle password reset email requests.
    """

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: PasswordResetRequestResponseSerializer},
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        return_url = serializer.validated_data["return_url"]

        user = get_user_model().objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{return_url}?uidb64={uidb64}&token={token}&email={email}"

        send_password_reset_email(user, reset_url)

        response_serializer = PasswordResetRequestResponseSerializer(
            data={"message": "Password reset email sent"}
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=200)


class PasswordResetConfirmView(APIView):
    """
    View to handle password reset confirmation.
    """

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: PasswordResetConfirmResponseSerializer},
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["password"]

        user.set_password(new_password)
        user.save()

        response_serializer = PasswordResetConfirmResponseSerializer(
            data={"message": "Password reset successful"}
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserListSerializer
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


class UserListRetrieveView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserListSerializer
    permission_classes = (AllowAny,)
    queryset = (
        User.objects.all()
        .select_related("social_links")
        .prefetch_related("albums", "followers", "genres")
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserRetrieveSerializer
        return UserListSerializer
