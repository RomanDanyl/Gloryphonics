from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import RegistrationApplicationViewSet, CreateUserView

app_name = "user"

router = DefaultRouter()
router.register("applications", RegistrationApplicationViewSet, basename="applications")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("", include(router.urls)),
]
