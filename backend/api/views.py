from django.contrib.auth import get_user_model
from django.http import FileResponse
from djoser.views import UserViewSet
from djoser import permissions
from rest_framework import status
from rest_framework.decorators import action
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    DestroyModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

from .constants import NO_SHOPPING_CART
from .mixins import post_delete_recipe
from .permissions import AuthorOrReadOnly
from .renderers import CSVCartDataRenderer, PlainTextRenderer
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
        return post_delete_recipe(
            self, request, Favorite, FavoriteSerializer
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return post_delete_recipe(
            self, request, ShoppingCart, ShoppingCartSerializer
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        renderer_classes=(CSVCartDataRenderer, PlainTextRenderer,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(author=request.user)
        if shopping_cart:
            serializer = (ShoppingCartSerializer(shopping_cart, many=True))
            file_name = f'shopping_cart.{request.accepted_renderer.format}'
            return Response(
                serializer.data,
                headers={
                    "Content-Disposition": f'attachment;filename="{file_name}"'
                }
            )
        else:
            return Response(
                NO_SHOPPING_CART,
                status=status.HTTP_400_BAD_REQUEST
            )


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
