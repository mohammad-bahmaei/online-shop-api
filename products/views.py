from django.shortcuts import get_object_or_404
from .serializer import ProductSerializers
from rest_framework.views import APIView 
from rest_framework.generics import  ListAPIView
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from django.core.cache import cache
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

class ProductAPIView(APIView):
    
    def get(self, request, slug):

        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializers(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductPagination(PageNumberPagination):

    page_size = 5


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related("images").order_by("-created_at", "-id")
    serializer_class = ProductSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "description"]
    filterset_fields = ["category"]
    ordering_fields = ["price", "created_at"]
    pagination_class = ProductPagination

    def list(self, request, *args, **kwargs):
        if request.query_params:
            return super().list(request, *args, **kwargs)
        
        cached_data = cache.get("product_list")
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set("product_list", response.data, 300)

        return response

