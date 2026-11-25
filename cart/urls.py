from .views import CartView, AddToCartAPIView
from django.urls import path

urlpatterns = [
path("", CartView.as_view(), name="cart"),
path("add/", AddToCartAPIView.as_view(), name="add_to_cart")
]
