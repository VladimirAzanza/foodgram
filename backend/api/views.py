from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
