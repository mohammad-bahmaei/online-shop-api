from .views import CartAPIView
from django.urls import path

urlpatterns = [
path("", CartView.as_view(), name="cart"),
]
