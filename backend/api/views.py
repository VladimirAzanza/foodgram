from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from djoser import permissions
from rest_framework import status
from rest_framework.decorators import action
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

from .constants import (
    RECIPE_ALREADY_ADDED,
    RECIPE_DELETED,
    NO_RECIPE
)
from .serializers import (
    AvatarCurrentUserSerializer,
    FavoriteSerializer,
    RecipeGetSerializer,
    RecipeLinkSerializer,
    RecipePostPutPatchSerializer,
    ShoppingCartSerializer,
    TagSerializer,
    IngredientSerializer
)
from .permissions import AuthorOrReadOnly
from tags.models import Tag
from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, ShoppingCart

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

    # corregir, crear un link short sin hyperlinked?
    @action(detail=True, url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        serializer = RecipeLinkSerializer(recipe, context={
            'request': request,
        })
        return Response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'POST':
            favorite_data, created_favorite = Favorite.objects.get_or_create(
                recipe=recipe, author=request.user
            )
            if created_favorite:
                response_data = FavoriteSerializer(favorite_data).data
                return Response(
                    response_data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    RECIPE_ALREADY_ADDED,
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            favorite_data = Favorite.objects.filter(
                recipe=recipe, author=self.request.user
            )
            if favorite_data:
                favorite_data.delete()
                return Response(
                    RECIPE_DELETED,
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                NO_RECIPE,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'POST':
            cart_data, created_cart = ShoppingCart.objects.get_or_create(
                recipe=recipe, author=request.user
            )
            if created_cart:
                response_data = ShoppingCartSerializer(cart_data).data
                return Response(
                    response_data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    RECIPE_ALREADY_ADDED,
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            cart_data = ShoppingCart.objects.filter(
                recipe=recipe, author=self.request.user
            )
            if cart_data:
                cart_data.delete()
                return Response(
                    RECIPE_DELETED,
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                NO_RECIPE,
                status=status.HTTP_400_BAD_REQUEST
            )


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
