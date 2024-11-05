from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.v1.fields import Base64ImageField
from recipes.models import Recipe
from users.models import Subscription

from .constants import (
    PROHIBITED_FIRST_NAME_MESSAGE,
    PROHIBITED_LAST_NAME_MESSAGE,
    PROHIBITED_USERNAME_MESSAGE
)
from .fields import is_user_is_subscribed
from .utils import validate_field

User = get_user_model()


class CustomCurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )
        read_only_fields = (
            'id',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return is_user_is_subscribed(
            self.context['request'].user, obj
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )

    def get_is_subscribed(self, obj):
        return is_user_is_subscribed(
            self.context['request'].user, obj
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        required_fields = (
            'password',
            'email',
            'username',
            'first_name',
            'last_name'
        )

    def validate_username(self, value):
        if not validate_field(value):
            raise serializers.ValidationError(PROHIBITED_USERNAME_MESSAGE)
        return value

    def validate_first_name(self, value):
        if not validate_field(value):
            raise serializers.ValidationError(PROHIBITED_FIRST_NAME_MESSAGE)
        return value

    def validate_last_name(self, value):
        if not validate_field(value):
            raise serializers.ValidationError(PROHIBITED_LAST_NAME_MESSAGE)
        return value


class RecipesToSubscriptions(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='following.email')
    id = serializers.IntegerField(source='following.id')
    username = serializers.CharField(source='following.username')
    first_name = serializers.CharField(source='following.first_name')
    last_name = serializers.CharField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='following.avatar')

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )
        validators = [UniqueTogetherValidator(
            queryset=Subscription.objects.all(),
            fields=('user', 'following')
        )]

    def get_is_subscribed(self, obj):
        return is_user_is_subscribed(
            obj.user, obj.following
        )

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.following)
        return RecipesToSubscriptions(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()


class AvatarCurrentUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)
