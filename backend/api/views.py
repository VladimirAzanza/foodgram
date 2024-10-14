from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import permissions
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

from djoser.views import UserViewSet
from djoser import permissions

from .serializers import AvatarCurrentUserSerializer, RecipeSerializer, TagSerializer
from .permissions import AuthorOrReadOnly
from tags.models import Tag
from recipes.models import Recipe

User = get_user_model()


class CurrentUserAvatar(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = AvatarCurrentUserSerializer
    permission_classes = (permissions.CurrentUserOrAdminOrReadOnly,)

    def get_object(self):
        return self.request.user


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
