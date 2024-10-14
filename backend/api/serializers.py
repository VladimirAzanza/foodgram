from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe
from tags.models import Tag

User = get_user_model()


class CustomUserSerializer(UserSerializer):
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


class CreateCustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }


class CustomCurrentUserSerializer(UserSerializer):
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


class AvatarCurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)
