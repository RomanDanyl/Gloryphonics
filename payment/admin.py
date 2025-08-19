from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "paypal_order_id",
        "user",
        "amount",
        "currency",
        "status",
        "created_at",
    )
    search_fields = ("paypal_order_id", "user__email")
    list_filter = ("status", "currency")
