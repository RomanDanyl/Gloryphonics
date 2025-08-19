from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Donation
from django.contrib.auth import get_user_model

from .services import create_donation

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def paypal_webhook(request):
    event_type = request.data.get("event_type")
    resource = request.data.get("resource", {})

    if event_type == "CHECKOUT.ORDER.APPROVED":
        order_id = resource.get("id")
        amount = resource.get("purchase_units", [{}])[0].get("amount", {}).get("value")
        currency = (
            resource.get("purchase_units", [{}])[0]
            .get("amount", {})
            .get("currency_code")
        )

        # Створити донат (без прив’язки до юзера — бо він анонімний)
        Donation.objects.update_or_create(
            paypal_order_id=order_id,
            defaults={"amount": amount, "currency": currency, "status": "APPROVED"},
        )

    elif event_type == "PAYMENT.CAPTURE.COMPLETED":
        capture_id = resource.get("id")
        order_id = (
            resource.get("supplementary_data", {})
            .get("related_ids", {})
            .get("order_id")
        )
        # Обновлюємо статус на COMPLETED
        Donation.objects.filter(paypal_order_id=order_id).update(status="COMPLETED")

    return Response(status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_donation_view(request):
    amount = request.data.get("amount", 5)
    return_url = "https://gloryphonic-site.com/donation-success"
    cancel_url = "https://gloryphonic-site.com/donation-cancel"

    data = create_donation(amount, return_url, cancel_url)
    approval_url = next(
        link["href"] for link in data["links"] if link["rel"] == "approve"
    )
    order_id = data["id"]

    # Зберігаємо попередній донат із прив'язкою до user
    Donation.objects.create(
        user=request.user if request.user.is_authenticated else None,
        paypal_order_id=order_id,
        amount=amount,
        currency="EUR",
        status="CREATED",
    )

    return Response({"approval_url": approval_url})
