from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import (
    CharField,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ImageField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from .fields import Base64ImageField, get_boolean
from recipes.models import (
    Favorite, IngredientRecipe, Recipe, ShoppingCart
)
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
            # 'is_subscribed',
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
            # 'is_subscribed',
            'avatar',
        )
        read_only_fields = (
            'id',
            # 'is_subscribed'
        )


class AvatarCurrentUserSerializer(ModelSerializer):
    avatar = Base64ImageField(required=True)

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


class IngredientRecipeCreateUpdateSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeGetSerializer(ModelSerializer):
    id = IntegerField(source='ingredient.id', read_only=True)
    name = CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount')


class RecipeGetSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeGetSerializer(
        source='ingredient_recipe', many=True
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

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
        return get_boolean(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return get_boolean(self, obj, ShoppingCart)


class RecipePostPutPatchSerializer(ModelSerializer):
    image = Base64ImageField(required=True)
    ingredients = IngredientRecipeCreateUpdateSerializer(
        many=True, required=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

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


class RecipeLinkSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('url',)
        extra_kwargs = {
            'url': {
                'view_name': 'recipe-detail',
                'lookup_field': 'pk',
                # to rest_framework settings:
                # 'url_field_name': 'short-link'
            }
        }


class CommonFavoriteCartSerializer(ModelSerializer):
    id = IntegerField(source='recipe.id', read_only=True)
    name = CharField(source='recipe.name', read_only=True)
    image = ImageField(source='recipe.image', read_only=True)
    cooking_time = IntegerField(source='recipe.cooking_time', read_only=True)


class FavoriteSerializer(CommonFavoriteCartSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(CommonFavoriteCartSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
