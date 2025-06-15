import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import User

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse('register')  # name used in your urls.py

    payload = {
        "email": "newuser@example.com",
        "password": "securepassword123"
    }

    response = client.post(url, payload, format='json')

    assert response.status_code == 201
    assert response.data['message'] == 'User registered successfully'


@pytest.mark.django_db
def test_login_success():
    User.objects.create_user(password='1234pass', email='t@test.com')

    client = APIClient()
    response = client.post('/api/login/', {
        'email': 't@test.com',
        'password': '1234pass'
    })

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

import pytest
from rest_framework.test import APIClient
from core.models import User

@pytest.mark.django_db
def test_token_refresh():

    User.objects.create_user(email='refresh@test.com', password='pass1234')
    client = APIClient()


    login_response = client.post('/api/login/', {
        'email': 'refresh@test.com',
        'password': 'pass1234'
    })

    assert login_response.status_code == 200
    refresh_token = login_response.data['refresh']
    assert refresh_token is not None

    refresh_response = client.post('/api/token/refresh/', {
        'refresh': refresh_token
    })

    assert refresh_response.status_code == 200
    assert 'access' in refresh_response.data
