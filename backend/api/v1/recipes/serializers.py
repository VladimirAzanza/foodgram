from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .utils import check_object_in_model, create_ingredient_recipe
from api.v1.fields import Base64ImageField
from api.v1.ingredients.serializers import (
    IngredientRecipeCreateUpdateSerializer, IngredientRecipeGetSerializer
)
from api.v1.tags.serializers import TagSerializer
from api.v1.users.serializers import CustomUserSerializer
from foodgram_backend.constants import (
    ADD_TAGS_MESSAGE,
    DO_NOT_REPEAT_TAGS_MESSAGE,
    ADD_INGREDIENTS_MESSAGE,
    DO_NOT_REPEAT_INGREDIENTS_MESSAGE
)
from recipes.models import Favorite, Recipe, ShoppingCart


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
        return check_object_in_model(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return check_object_in_model(self, obj, ShoppingCart)


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
            'cooking_time': {'required': True},
        }

    def validate_tags(self, value):
        if not value:
            raise ValidationError(ADD_TAGS_MESSAGE)
        if len(value) != len(set(value)):
            raise ValidationError(DO_NOT_REPEAT_TAGS_MESSAGE)
        return value

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError(ADD_INGREDIENTS_MESSAGE)
        seen_ingredient_ids = set()
        for ingredient in value:
            ingredient_id = ingredient['id']
            if ingredient_id in seen_ingredient_ids:
                raise ValidationError(
                    DO_NOT_REPEAT_INGREDIENTS_MESSAGE
                )
            seen_ingredient_ids.add(ingredient_id)
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = Recipe.objects.create(**validated_data)
        instance.tags.set(tags)
        create_ingredient_recipe(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        instance.ingredients.clear()
        create_ingredient_recipe(instance, ingredients)
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
