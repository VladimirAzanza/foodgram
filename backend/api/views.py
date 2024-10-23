from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from djoser import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    DestroyModelMixin, UpdateModelMixin
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

from .constants import (
    ALREADY_SUBSCRIBED,
    CANNOT_SUBSCRIBE_TO_YOURSELF,
    NO_SHOPPING_CART,
    NO_SUBSCRIPTION
)
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
    SubscriptionSerializer,
    TagSerializer,
    IngredientSerializer
)
from tags.models import Tag
from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, ShoppingCart
from users.models import Subscription

User = get_user_model()


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
        filter_Q = Q()
        if is_favorited == '1':
            filter_Q &= Q(favorite__author=user)
        elif is_favorited == '0':
            filter_Q &= ~Q(favorite__author=user)

        if is_in_shopping_cart == '1':
            filter_Q &= Q(shopping_cart__author=user)
        elif is_in_shopping_cart == '0':
            filter_Q &= ~Q(shopping_cart__author=user)
        return queryset.filter(filter_Q)

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
