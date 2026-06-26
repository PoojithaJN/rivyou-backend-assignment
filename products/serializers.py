from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SearchResultSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    product = ProductSerializer()
