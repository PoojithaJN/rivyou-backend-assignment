import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='password123', email='test@test.com')
    return user

@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'password123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert 'token' in response.data

@pytest.mark.django_db
def test_login_user(api_client, create_user):
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'token' in response.data

@pytest.mark.django_db
def test_logout_user(api_client, create_user):
    # First login
    login_url = reverse('login')
    data = {'username': 'testuser', 'password': 'password123'}
    response = api_client.post(login_url, data, format='json')
    
    refresh_token = response.data['refresh']
    access_token = response.data['token']
    
    # Then logout
    logout_url = reverse('logout')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    logout_response = api_client.post(logout_url, {'refresh': refresh_token}, format='json')
    
    assert logout_response.status_code == 200
