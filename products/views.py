from django.shortcuts import get_object_or_404
from .serializer import ProductSerializers
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from django.core.cache import cache

class ProductAPIView(APIView):
    
    def get(self, request, slug):

        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializers(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPIView(APIView):

    def get(self, request):
        products = cache.get("product_list")

        if products is None:
            print("CACHE MISS")

            products = Product.objects.all()
            serializer = ProductSerializers(products, many=True)
            products = serializer.data
            cache.set("product_list", products, 300)

        else:
            print("CACHE HIT")

        return Response(products, status=status.HTTP_200_OK)