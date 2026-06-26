import pytest
from django.urls import reverse
from products.models import Product
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, db):
    user = User.objects.create_user(username='testuser', password='password123')
    response = api_client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'}, format='json')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['token'])
    return api_client

@pytest.fixture
def create_products(db):
    Product.objects.create(
        product_name="Phone 1",
        product_description="A good phone",
        category="Smartphones",
        tags=["camera", "5g"]
    )
    Product.objects.create(
        product_name="Phone Charger",
        product_description="Charger for smartphone",
        category="Chargers",
        tags=["fast-charging", "smartphone"]
    )
    Product.objects.create(
        product_name="Back Cover",
        product_description="Smartphone cover",
        category="Accessories",
        tags=["cover"]
    )

@pytest.mark.django_db
def test_search_ranking(auth_client, create_products):
    url = reverse('product-search') + '?q=smartphone'
    response = auth_client.get(url)
    
    assert response.status_code == 200
    results = response.data
    
    # Check if paginated
    if 'results' in results:
        results = results['results']
        
    assert len(results) > 0
    
    # Category match should be first
    assert results[0]['product']['category'] == 'Smartphones'
    assert results[0]['score'] == 100
    
    # Tag match or description match should follow
    assert results[1]['product']['category'] == 'Chargers'
    assert results[1]['score'] == 70

@pytest.mark.django_db
def test_category_api(auth_client, create_products):
    url = reverse('product-category', args=['Smartphones'])
    response = auth_client.get(url)
    assert response.status_code == 200
    
    # Check if paginated
    results = response.data
    if 'results' in results:
        results = results['results']
        
    assert len(results) == 1
    assert results[0]['category'] == 'Smartphones'
