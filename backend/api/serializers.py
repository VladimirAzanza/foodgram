from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ingredients.models import Ingredient
from recipes.models import Favorite, IngredientRecipe, Recipe, ShoppingCart
from tags.models import Tag
from users.models import Subscription

from .fields import (Base64ImageField, get_boolean_if_favorited_or_in_cart,
                     get_boolean_if_user_is_subscribed)

User = get_user_model()


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
        user = self.context['request'].user
        return get_boolean_if_user_is_subscribed(user, obj)


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
            'password': {
                'required': True,
                'allow_blank': False
            },
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': UniqueValidator(queryset=User.objects.all())
            },
            'username': {
                'required': True, 'allow_blank': False
            },
            'first_name': {
                'required': True, 'allow_blank': False
            },
            'last_name': {
                'required': True, 'allow_blank': False
            },
        }


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
        user = self.context['request'].user
        return get_boolean_if_user_is_subscribed(user, obj)


class AvatarCurrentUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id', read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name', read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeGetSerializer(
        source='ingredient_recipe', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return get_boolean_if_favorited_or_in_cart(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return get_boolean_if_favorited_or_in_cart(self, obj, ShoppingCart)


class RecipePostPutPatchSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    ingredients = IngredientRecipeCreateUpdateSerializer(
        many=True, required=True
    )

    class Meta:
        model = Recipe
        exclude = ('created_at',)
        read_only_fields = ('author',)
        extra_kwargs = {
            'name': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True},
        }

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.add(*tags)
        if ingredients is not None:
            for ingredient in ingredients:
                IngredientRecipe.objects.get_or_create(
                    recipe=instance,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
        instance.save()
        return instance


class CommonFavoriteCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='recipe.id', read_only=True
    )
    name = serializers.CharField(
        source='recipe.name', read_only=True
    )
    image = serializers.ImageField(
        source='recipe.image', read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )


class FavoriteSerializer(CommonFavoriteCartSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(CommonFavoriteCartSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


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

    def get_is_subscribed(self, obj):
        user = obj.user
        following = obj.following
        return get_boolean_if_user_is_subscribed(user, following)

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.following)
        return RecipesToSubscriptions(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()
