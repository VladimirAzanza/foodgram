from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from djoser import permissions
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

from .serializers import (
    AvatarCurrentUserSerializer,
    RecipeGetSerializer,
    RecipeLinkSerializer,
    RecipePostPutPatchSerializer,
    TagSerializer,
    IngredientSerializer
)
from .permissions import AuthorOrReadOnly
from tags.models import Tag
from ingredients.models import Ingredient
from recipes.models import Recipe

User = get_user_model()


class CustomCurrentUser(UserViewSet):
    permission_classes = (permissions.CurrentUserOrAdmin,)


class CurrentUserAvatar(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = AvatarCurrentUserSerializer
    permission_classes = (permissions.CurrentUserOrAdminOrReadOnly,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.avatar.delete()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipePostPutPatchSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeLinkViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = RecipeLinkSerializer

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('id'))


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
