from http import HTTPStatus

import pytest

from .constants import IMAGE, NAME_RECIPE, TEXT_RECIPE, COOKING_TIME
from recipes.models import Recipe


@pytest.mark.django_db
def test_data_for_post_recipe(
    author_client,
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
    response = author_client.post(
        recipe_list_url, data, format='json'
    )
    assert response.status_code == HTTPStatus.CREATED
    created_recipe = Recipe.objects.get(id=response.data['id'])
    assert created_recipe.name == data['name']
    assert created_recipe.text == data['text']
    assert created_recipe.cooking_time == data['cooking_time']
    assert created_recipe.ingredients.count() == len(ingredient_data)
    assert created_recipe.tags.count() == len(tags_ids)
