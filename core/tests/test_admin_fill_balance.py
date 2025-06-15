from core.models import User
from core.models import BankAccount
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_admin_fill_balance():
    admin = User.objects.create_superuser(email="admin@test.com", password="admin")
    user = User.objects.create_user(email="user@test.com", password="user")
    BankAccount.objects.create(user=user, balance=0.0)

    client = APIClient()
    response = client.post(
        "/api/login/",
        {
            "email": "admin@test.com",
            "password": "admin",
        },
    )
    assert response.status_code == 200
    token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    payload = {"email": "user@test.com", "amount": "100.00"}

    response = client.post("/api/admin/add-balance/", payload, format="json")

    assert response.status_code == 200
    assert "100.00 added to" in response.data["message"]

    user.refresh_from_db()

    account = BankAccount.objects.get(user=user)
    assert account.balance == 100.0
