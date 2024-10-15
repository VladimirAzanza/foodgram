from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)
# borrar esto:
from djoser.views import UserViewSet
from djoser import permissions

from .serializers import (
    AvatarCurrentUserSerializer,
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer
)
from .permissions import AuthorOrReadOnly
from tags.models import Tag
from ingredients.models import Ingredient
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


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
