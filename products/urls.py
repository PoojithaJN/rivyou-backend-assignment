from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryAPIView, SearchAPIView

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='product-search'),
    path('category/<str:category_name>/', CategoryAPIView.as_view(), name='product-category'),
    path('', include(router.urls)),
]
