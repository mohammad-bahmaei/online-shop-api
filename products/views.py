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

class ProductAPIView(APIView):
    
    def get(self, request, slug):

        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializers(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class ProductListAPIView(ListAPIView):

#     filter_backends = [SearchFilter]
#     search_fields = ["name", "description"]

#     def get(self, request):
#         products = cache.get("product_list")

#         if products is None:
#             print("CACHE MISS")

#             products = Product.objects.prefetch_related("images")
#             serializer = ProductSerializers(products, many=True)
#             products = serializer.data
#             cache.set("product_list", products, 300)

#         else:
#             print("CACHE HIT")

#         return Response(products, status=status.HTTP_200_OK)

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related("images")
    serializer_class = ProductSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "description"]
    filterset_fields = ["category"]

 