from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        return User.objects.all()
