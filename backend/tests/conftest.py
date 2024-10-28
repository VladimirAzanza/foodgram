import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ingredients.models import Ingredient
from recipes.models import IngredientRecipe, Recipe
from tags.models import Tag

from .constants import (AUTHOR_USERNAME, COOKING_TIME, EMAIL_AUTHOR,
                        EMAIL_NOT_AUTHOR, IMAGE, NAME_RECIPE,
                        NOT_AUTHOR_USERNAME, TEXT_RECIPE)


@pytest.fixture
def author(django_user_model):
    user = django_user_model.objects.create(
        email=EMAIL_AUTHOR,
        username=AUTHOR_USERNAME
    )
    Token.objects.create(user=user)
    return user


@pytest.fixture
def not_author(django_user_model):
    user = django_user_model.objects.create(
        email=EMAIL_NOT_AUTHOR,
        username=NOT_AUTHOR_USERNAME
    )
    Token.objects.create(user=user)
    return user


@pytest.fixture
def author_client(author):
    client = APIClient()
    client.force_authenticate(user=author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = APIClient()
    client.force_authenticate(user=not_author)
    return client


@pytest.fixture
def create_ingredients():
    ingredients = [Ingredient(
        name=f'ingredient {n}',
        measurement_unit='gr'
    ) for n in range(1, 4)]
    Ingredient.objects.bulk_create(ingredients)
    return ingredients


@pytest.fixture
def create_tags():
    tags = [
        Tag(
            name=f'Tag {n}',
            slug=f'tag_{n}'
        )
        for n in range(1, 4)
    ]
    Tag.objects.bulk_create(tags)
    return tags


@pytest.fixture
def recipe_by_author(author, create_ingredients, create_tags):
    recipe = Recipe.objects.create(
        author=author,
        image=IMAGE,
        name=NAME_RECIPE,
        text=TEXT_RECIPE,
        cooking_time=COOKING_TIME
    )
    for ingredient in create_ingredients:
        IngredientRecipe.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=5
        )
    recipe.tags.set(create_tags)
    return recipe


@pytest.fixture
def users_list_url():
    return reverse('api_v1:users-list')


@pytest.fixture
def tag_list_url():
    return reverse('api_v1:tag-list')


@pytest.fixture
def recipe_list_url():
    return reverse('api_v1:recipe-list')


@pytest.fixture
def ingredient_list_url():
    return reverse('api_v1:ingredient-list')


@pytest.fixture
def users_me_url():
    return reverse('api_v1:users-me', args=())


@pytest.fixture
def not_author_user_url(not_author):
    return reverse('api_v1:users-detail', args=(not_author.id,))


@pytest.fixture
def get_ingredient(create_ingredients):
    return reverse(
        'api_v1:ingredient-detail', args=(create_ingredients[0].id,)
    )


@pytest.fixture
def get_tag(create_tags):
    return reverse('api_v1:tag-detail', args=(create_tags[0].id,))


@pytest.fixture
def get_recipe_url(recipe_by_author):
    return reverse('api_v1:recipe-detail', args=(recipe_by_author.id,))


@pytest.fixture
def post_delete_subscribe_url(author):
    return reverse('api_v1:users-subscribe', args=(author.id,))


@pytest.fixture
def post_delete_favorite_url(recipe_by_author):
    return reverse('api_v1:recipe-favorite', args=(recipe_by_author.id,))
