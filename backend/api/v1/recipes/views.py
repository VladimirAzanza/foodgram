import os

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.recipes.permissions import AuthorOrReadOnly
from recipes.models import Favorite, Recipe, ShoppingCart

from .constants import NO_SHOPPING_CART
from .mixins import post_delete_recipe
from .renderers import CSVCartDataRenderer, PlainTextRenderer
from .serializers import (FavoriteSerializer, RecipeGetSerializer,
                          RecipePostPutPatchSerializer, ShoppingCartSerializer)

load_dotenv()


class RecipeViewSet(ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        is_favorited = self.request.query_params.get(
            'is_favorited'
        )
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        tags = self.request.query_params.getlist(
            'tags'
        )
        filter_Q = Q()
        if is_favorited == '1':
            filter_Q &= Q(favorite__author=user)
        elif is_favorited == '0':
            filter_Q &= ~Q(favorite__author=user)

        if is_in_shopping_cart == '1':
            filter_Q &= Q(shopping_cart__author=user)
        elif is_in_shopping_cart == '0':
            filter_Q &= ~Q(shopping_cart__author=user)

        if tags:
            filter_Q &= Q(tags__slug__in=tags)
        return queryset.filter(filter_Q).distinct()

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
        short_link_2 = f'{frontend_url}/{url_to_recipes}/{id_recipe}/'
        return Response({"short-link": short_link_2})

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
        data = []
        ingredients_added = {}
        if shopping_cart:
            for element in shopping_cart:
                ingredients_in_recipe = element.recipe.ingredient_recipe.all()
                for ingredient_in_recipe in ingredients_in_recipe:
                    ingredient = ingredient_in_recipe.ingredient
                    amount = ingredient_in_recipe.amount
                    if ingredient.name not in ingredients_added:
                        ingredients_added[ingredient.name] = {
                            'Число': amount,
                            'Измерение': ingredient.measurement_unit
                        }
                    else:
                        ingredients_added[ingredient.name]['Число'] += amount
            for ingredient, total in ingredients_added.items():
                data.append({
                    'Ингредиенты': ingredient,
                    'Число': total['Число'],
                    'Измерение': total['Измерение']
                })
            file_name = f'shopping_cart.{request.accepted_renderer.format}'
            return Response(
                data,
                headers={
                    "Content-Disposition": f'attachment;filename="{file_name}"'
                }
            )
        else:
            return Response(
                NO_SHOPPING_CART,
                status=status.HTTP_400_BAD_REQUEST
            )
