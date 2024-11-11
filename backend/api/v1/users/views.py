from djoser import permissions
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    AvatarCurrentUserSerializer,
    RecipesToSubscriptions,
    SubscriptionSerializer
)
from .utils import get_subscriptions_data
from api.v1.pagination import LimitSetPagination
from foodgram_backend.constants import (
    ALREADY_SUBSCRIBED,
    CANNOT_SUBSCRIBE_TO_YOURSELF,
    NO_SUBSCRIPTION
)
from recipes.models import Recipe
from users.models import Subscription


class CustomUserViewSet(DjoserUserViewSet):
    @action(
        methods=['get', 'put', 'patch', 'delete'],
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
        limit = request.query_params.get('limit')
        recipes_limit = request.query_params.get('recipes_limit')
        if not limit:
            serializer_data = get_subscriptions_data(
                user_profile,
                SubscriptionSerializer,
                Recipe,
                RecipesToSubscriptions,
                recipes_limit
            )
            return Response(serializer_data)
        pagination = LimitSetPagination()
        pagination_subscriptions = pagination.paginate_queryset(
            queryset=user_profile, request=request
        )
        if recipes_limit:
            serializer_data = get_subscriptions_data(
                pagination_subscriptions,
                SubscriptionSerializer,
                Recipe,
                RecipesToSubscriptions,
                recipes_limit
            )
            return pagination.get_paginated_response(serializer_data)
        serializer = SubscriptionSerializer(
            pagination_subscriptions, many=True
        )
        return pagination.get_paginated_response(serializer.data)

    @action(
        methods=['post'],
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

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk=None):
        subscription = Subscription.objects.filter(
            user=request.user, following=self.get_object()
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
