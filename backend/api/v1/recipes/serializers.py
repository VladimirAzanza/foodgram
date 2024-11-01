from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.v1.fields import Base64ImageField
from api.v1.ingredients.serializers import (
    IngredientRecipeCreateUpdateSerializer, IngredientRecipeGetSerializer)
from api.v1.tags.serializers import TagSerializer
from api.v1.users.serializers import CustomUserSerializer
from recipes.models import Favorite, IngredientRecipe, Recipe, ShoppingCart

from .fields import get_boolean_if_favorited_or_in_cart


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
            instance.tags.set(tags)
        if ingredients is not None:
            instance.ingredients.clear()
            for ingredient in ingredients:
                IngredientRecipe.objects.create(
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
        validators = [UniqueTogetherValidator(
            queryset=Favorite.objects.all(),
            fields=('recipe', 'author')
        )]


class ShoppingCartSerializer(CommonFavoriteCartSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
        validators = [UniqueTogetherValidator(
            queryset=ShoppingCart.objects.all(),
            fields=('recipe', 'author')
        )]
