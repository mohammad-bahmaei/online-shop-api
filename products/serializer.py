from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "is_primary",
        ]


class ProductSerializers(serializers.ModelSerializer):

    images = ProductImageSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "price",
            "stock",
            "discount_price",
            "slug",
            "description",
            "is_active",
            "created_at",
            "images",
        ]