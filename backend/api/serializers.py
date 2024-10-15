from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import PrimaryKeyRelatedField, ModelSerializer, SerializerMethodField

from .fields import Base64ImageField
from recipes.models import Recipe, IngredientRecipe
from tags.models import Tag
from ingredients.models import Ingredient

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


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(ModelSerializer):
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('ingredient', 'amount')

    def create(self, validated_data):
        print(f'validated_data 1: {validated_data}')
        ingredient = validated_data.pop('ingredient')
        ingredient_recipe = IngredientRecipe.objects.create(
            ingredient=ingredient, **validated_data
        )
        return ingredient_recipe


class RecipeSerializer(ModelSerializer):
    image = Base64ImageField(required=True)
    ingredients = IngredientRecipeSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def create(self, validated_data):
        print(f'validated_data 2: {validated_data}')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        print(f'impresion tags: {tags}')
        print(f'impresion ingredients: {ingredients}')
        recipe.tags.set(tags)
        for ingredient in ingredients:
            print(ingredient['ingredient'])
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
        return recipe
