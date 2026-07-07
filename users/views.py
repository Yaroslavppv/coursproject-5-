from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer

# Create your views here.
class RegisterView(CreateAPIView):
    """Регистрация нового пользователя (доступно всем)"""
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]