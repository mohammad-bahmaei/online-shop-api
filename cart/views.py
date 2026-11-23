from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializer import CartSerializer, AddToCartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CartView(RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_Item = CartItem.objects.filter(cart=cart, product=product).first()
        
        if cart_Item:
            cart_Item.quantity += quantity
            cart_Item.save()
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return Response(
            {"message": "محصول شما با موفقیت اضافه شد"},
            status=status.HTTP_200_OK
        )

    