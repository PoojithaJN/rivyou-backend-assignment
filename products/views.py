from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, SearchResultSerializer
from .utils import correct_typo
from django.db.models import Q
import json

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CategoryAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category_name']
        return Product.objects.filter(category__iexact=category)

class SearchAPIView(generics.ListAPIView):
    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        # Typo correction using RapidFuzz
        corrected_query = correct_typo(query)
        q_lower = corrected_query.lower()

        # Fetch all products (dataset is small, ~1000 items, memory ranking is fast)
        # Using exact matching per rules to ensure correct prioritization
        products = Product.objects.all()
        results = []
        
        for product in products:
            score = 0
            
            # Check category match
            if product.category and q_lower in product.category.lower():
                score = max(score, 100)
            
            # Check tag match
            tags = product.tags
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags.replace("'", '"'))
                except:
                    tags = [t.strip() for t in tags.split(',')]
            
            if isinstance(tags, list):
                if any(q_lower in str(t).lower() for t in tags):
                    score = max(score, 70)
            elif isinstance(tags, str):
                if q_lower in tags.lower():
                    score = max(score, 70)

            # Check name match
            if product.product_name and q_lower in product.product_name.lower():
                score = max(score, 40)
            
            # Check description match
            if product.product_description and q_lower in product.product_description.lower():
                score = max(score, 30)
                
            if score > 0:
                results.append({
                    'score': score,
                    'product': product
                })

        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
