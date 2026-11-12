from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer, LoginSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView

class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    