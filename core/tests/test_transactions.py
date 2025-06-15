import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import User, BankAccount, Transaction

@pytest.mark.django_db
def test_user_to_user_transaction_direction():
    client = APIClient()

    sender = User.objects.create_user(email="sender@test.com", password="pass123")
    receiver = User.objects.create_user(email="receiver@test.com", password="pass123")

    BankAccount.objects.create(user=sender, balance=100)
    BankAccount.objects.create(user=receiver, balance=50)

    client.force_authenticate(user=sender)

    response = client.post(reverse('user_to_user_transaction'), {
        "receiver_email": receiver.email,
        "amount": "10.00"
    })

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(reverse('get_transactions'))
    assert response.status_code == status.HTTP_200_OK
    sender_tx = response.data[0]
    assert sender_tx['direction'] == 'outcome'
    assert sender_tx['sender'] == sender.email
    assert sender_tx['receiver'] == receiver.email

    client.force_authenticate(user=receiver)
    response = client.get(reverse('get_transactions'))
    assert response.status_code == status.HTTP_200_OK
    receiver_tx = response.data[0]
    assert receiver_tx['direction'] == 'income'
    assert receiver_tx['sender'] == sender.email
    assert receiver_tx['receiver'] == receiver.email
