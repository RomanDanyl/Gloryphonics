from django.conf import settings
from django.contrib.sites import requests

PAYPAL_API = "https://api-m.sandbox.paypal.com"  # або live
CLIENT_ID = settings.PAYPAL_CLIENT_ID
CLIENT_SECRET = settings.PAYPAL_CLIENT_SECRET


def get_paypal_access_token():
    res = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
    )
    res.raise_for_status()
    return res.json()["access_token"]


def create_donation(amount, return_url, cancel_url):
    token = get_paypal_access_token()
    res = requests.post(
        f"{PAYPAL_API}/v2/checkout/orders",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {"amount": {"currency_code": "EUR", "value": str(amount)}}
            ],
            "application_context": {"return_url": return_url, "cancel_url": cancel_url},
        },
    )
    res.raise_for_status()
    return res.json()
