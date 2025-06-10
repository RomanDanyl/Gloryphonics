from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import RegistrationApplicationViewSet

app_name = "user"

router = DefaultRouter()
router.register("applications", RegistrationApplicationViewSet, basename="applications")

urlpatterns = [
    path("", include(router.urls)),
]
