from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    paypal_order_id = models.CharField(max_length=128, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="EUR")
    status = models.CharField(max_length=50)  # Наприклад: CREATED, COMPLETED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation {self.amount} {self.currency} - {self.status}"
