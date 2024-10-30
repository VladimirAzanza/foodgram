from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import get_boolean_if_user_is_subscribed
from recipes.models import Recipe
from users.models import Subscription
from api.fields import Base64ImageField
from api.v1.recipes.serializers import RecipesToSubscriptions

User = get_user_model()


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

    def get_is_subscribed(self, obj):
        user = obj.user
        following = obj.following
        return get_boolean_if_user_is_subscribed(user, following)

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