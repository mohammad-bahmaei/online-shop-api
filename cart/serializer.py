from rest_framework import serializers 
from .models import CartItem, Cart
from products.serializer import ProductSerializers

class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializers(read_only=True)
    
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "created_at", "updated_at", "items"]

class AddToCartSerializer(serializers.Serializer):
    
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)