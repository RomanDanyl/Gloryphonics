from django.urls import path
from .views import create_donation_view, paypal_webhook


app_name = "payment"

urlpatterns = [
    path("donate/", create_donation_view),
    path("webhook/", paypal_webhook),
]
