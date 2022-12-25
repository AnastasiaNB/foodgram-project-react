from djoser.views import UserViewSet
from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly)
from .models import User
from .serializers import CustomUserSerializer

class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]


