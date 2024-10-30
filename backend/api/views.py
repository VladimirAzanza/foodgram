import os

from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from djoser import permissions
from djoser.views import UserViewSet
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, ShoppingCart
from tags.models import Tag
from users.models import Subscription

from .constants import (ALREADY_SUBSCRIBED, CANNOT_SUBSCRIBE_TO_YOURSELF,
                        NO_SHOPPING_CART, NO_SUBSCRIPTION)
from .mixins import post_delete_recipe
from .permissions import AuthorOrReadOnly
from .renderers import CSVCartDataRenderer, PlainTextRenderer
from .serializers import (AvatarCurrentUserSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeGetSerializer,
                          RecipePostPutPatchSerializer, RecipesToSubscriptions,
                          ShoppingCartSerializer, SubscriptionSerializer,
                          TagSerializer)

User = get_user_model()
load_dotenv()


class CustomUserViewSet(UserViewSet):
    @action(
        methods=["get", "put", "patch", "delete"],
        detail=False,
        permission_classes=(permissions.CurrentUserOrAdmin,)
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request, pk=None):
        user_profile = request.user.followers.all()
        pagination = LimitOffsetPagination()
        pagination_subscriptions = pagination.paginate_queryset(
            queryset=user_profile, request=request
        )
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            serializer_data = []
            for information in pagination_subscriptions:
                serializer = SubscriptionSerializer(information).data
                recipes = Recipe.objects.filter(author=information.following)
                recipes = recipes[:int(recipes_limit)]
                serializer['recipes'] = RecipesToSubscriptions(
                    recipes, many=True
                ).data
                serializer_data.append(serializer)
            return pagination.get_paginated_response(serializer_data)
        serializer = SubscriptionSerializer(
            pagination_subscriptions, many=True
        )
        return pagination.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk=None):
        person_to_follow = self.get_object()
        user = request.user
        if user == person_to_follow:
            return Response(
                CANNOT_SUBSCRIBE_TO_YOURSELF,
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            subscription, data_created = Subscription.objects.get_or_create(
                user=user, following=person_to_follow
            )
            if data_created:
                response_data = SubscriptionSerializer(subscription).data
                return Response(
                    response_data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    ALREADY_SUBSCRIBED,
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                user=user, following=person_to_follow
            )
            if subscription:
                subscription.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                NO_SUBSCRIPTION,
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserAvatar(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = AvatarCurrentUserSerializer
    permission_classes = (permissions.CurrentUserOrAdmin,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.avatar.delete()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


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
        tags = self.request.query_params.get(
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
            filter_Q &= Q(tags__slug=tags)
        return queryset.filter(filter_Q)

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
            )user
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
