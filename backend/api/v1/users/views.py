from djoser import permissions
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from recipes.models import Recipe
from users.models import Subscription

from .constants import (ALREADY_SUBSCRIBED, CANNOT_SUBSCRIBE_TO_YOURSELF,
                        NO_SUBSCRIPTION)
from .serializers import (AvatarCurrentUserSerializer, RecipesToSubscriptions,
                          SubscriptionSerializer)


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
