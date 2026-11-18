from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializer import CartSerializer

class CartView(RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


    