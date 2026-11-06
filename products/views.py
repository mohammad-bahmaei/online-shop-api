from .serializer import ProductSerializers
from rest_framework.generics import  ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Product
from django.core.cache import cache
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

class ProductAPIView(RetrieveAPIView):
    
        queryset = Product.objects.prefetch_related("images")
        serializer_class = ProductSerializers
        lookup_field = "slug"

        def retrieve(self, request, *args, **kwargs):
             cache_key = f"product_{self.kwargs['slug']}"
             cache_data = cache.get(cache_key)
             
             if cache_data is not None:
                  print("CACHE HIT ")
                  return Response(cache_data)
             
             print("CACHE MISS")
             response = super().retrieve(request, *args, **kwargs)
             cache.set(cache_key, response.data, 300)
             
             return response
        
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
            print("CACHE HIT")
            return Response(cached_data)
        
        print("CACHE MISS")
        response = super().list(request, *args, **kwargs)
        cache.set("product_list", response.data, 300)
        return response

