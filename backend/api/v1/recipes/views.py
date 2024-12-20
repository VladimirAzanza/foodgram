import os

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import RecipeFilters
from .mixins import delete_recipe, post_recipe
from .renderers import CSVCartDataRenderer, PDFRenderer, PlainTextRenderer
from .serializers import (
    FavoriteSerializer,
    RecipeGetSerializer,
    RecipePostPutPatchSerializer,
    ShoppingCartSerializer
)
from api.v1.recipes.permissions import AuthorOrReadOnly
from foodgram_backend.constants import (
    MESSAGES,
    RECIPE_INGREDIENT_AMOUNT_PATH,
    RECIPE_INGREDIENT_MEASUREMENT_UNIT_PATH,
    RECIPE_INGREDIENT_NAME_PATH
)
from recipes.models import Favorite, Recipe, ShoppingCart

load_dotenv()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilters

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipePostPutPatchSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, url_path='get-link')
    def get_link(self, request, pk=None):
        id_recipe = self.kwargs[self.lookup_field]
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        url_to_recipes = os.getenv('URL_TO_RECIPES', 'recipes')
        short_link = f'{frontend_url}/{url_to_recipes}/{id_recipe}/'
        return Response({'short-link': short_link})

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return post_recipe(
            model=Favorite,
            serializer=FavoriteSerializer,
            recipe=self.get_object(),
            author=request.user
        )

    @favorite.mapping.delete
    def unfavorite(self, request, pk=None):
        return delete_recipe(
            model=Favorite,
            recipe=self.get_object(),
            author=request.user
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return post_recipe(
            model=ShoppingCart,
            serializer=ShoppingCartSerializer,
            recipe=self.get_object(),
            author=request.user
        )

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        return delete_recipe(
            model=ShoppingCart,
            recipe=self.get_object(),
            author=request.user
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        renderer_classes=(
            PDFRenderer, PlainTextRenderer, CSVCartDataRenderer
        )
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(author=request.user)
        if shopping_cart.exists():
            ingredient_data = shopping_cart.values(
                RECIPE_INGREDIENT_NAME_PATH,
                RECIPE_INGREDIENT_MEASUREMENT_UNIT_PATH
            ).annotate(
                total=Sum(RECIPE_INGREDIENT_AMOUNT_PATH)
            )
            data = [
                {
                    'Ингредиенты': ingredient[
                        RECIPE_INGREDIENT_NAME_PATH
                    ],
                    'Число': ingredient[
                        'total'
                    ],
                    'Измерение': ingredient[
                        RECIPE_INGREDIENT_MEASUREMENT_UNIT_PATH
                    ]
                } for ingredient in ingredient_data
            ]
            file_name = f'shopping_cart.{request.accepted_renderer.format}'
            return Response(
                data,
                headers={
                    'Content-Disposition': f'attachment;filename="{file_name}"'
                }
            )
        else:
            return Response(
                MESSAGES['no_shopping_cart'],
                status=status.HTTP_400_BAD_REQUEST
            )
