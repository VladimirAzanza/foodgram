from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from recipes.models import Recipe

from .constants import COOKING_TIME, IMAGE, NAME_RECIPE, TEXT_RECIPE


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status',
    (
        (lazy_fixture('author_client'), HTTPStatus.CREATED),
        (lazy_fixture('client'), HTTPStatus.UNAUTHORIZED)
    )
)
def test_post_recipe(
    user,
    status,
    recipe_list_url,
    create_ingredients,
    create_tags
):
    ingredient_data = [
        {
            'id': ingredient.id, 'amount': 10
        } for ingredient in create_ingredients
    ]
    tags_ids = [tag.id for tag in create_tags]
    data = {
        'ingredients': ingredient_data,
        'tags': tags_ids,
        'image': IMAGE,
        'name': NAME_RECIPE,
        'text': TEXT_RECIPE,
        'cooking_time': COOKING_TIME
    }
    response = user.post(
        recipe_list_url, data, format='json'
    )
    assert response.status_code == status
    if status == HTTPStatus.CREATED:

        created_recipe = Recipe.objects.get(id=response.data['id'])
        assert created_recipe.name == data['name']
        assert created_recipe.text == data['text']
        assert created_recipe.cooking_time == data['cooking_time']
        assert created_recipe.ingredients.count() == len(ingredient_data)
        assert created_recipe.tags.count() == len(tags_ids)


@pytest.mark.django_db
def test_post_recipe_with_invalid_data(
    author_client,
    recipe_list_url,
):
    data = {
        'image': IMAGE,
        'name': NAME_RECIPE,
        'text': TEXT_RECIPE,
        'cooking_time': COOKING_TIME
    }
    response = author_client.post(
        recipe_list_url, data, format='json'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

