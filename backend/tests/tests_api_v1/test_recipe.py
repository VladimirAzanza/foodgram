from http import HTTPStatus

from django.conf import settings
import pytest
from pytest_lazyfixture import lazy_fixture

from recipes.models import Recipe

from .constants import COOKING_TIME, DATA, IMAGE, NAME_RECIPE, TEXT_RECIPE


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
def test_post_recipe_with_invalid_data(author_client, recipe_list_url):
    data = DATA
    response = author_client.post(
        recipe_list_url, data, format='json'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status',
    (
        (lazy_fixture('author_client'), HTTPStatus.OK),
        (lazy_fixture('client'), HTTPStatus.UNAUTHORIZED)
    )
)
def test_patch_recipe(user, status, get_recipe_url):
    data = DATA
    response = user.patch(
        get_recipe_url, data, format='json'
    )
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status',
    (
        (lazy_fixture('author_client'), HTTPStatus.NO_CONTENT),
        (lazy_fixture('client'), HTTPStatus.UNAUTHORIZED)
    )
)
def test_delete_recipe(user, status, get_recipe_url):
    response = user.delete(get_recipe_url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status_post, status_delete',
    (
        (
            lazy_fixture('author_client'),
            HTTPStatus.CREATED,
            HTTPStatus.NO_CONTENT
        ),
        (
            lazy_fixture('not_author_client'),
            HTTPStatus.CREATED,
            HTTPStatus.NO_CONTENT
        )
    )
)
def test_post_delete_recipe_shopping_cart(
    user,
    status_post,
    status_delete,
    post_delete_recipe_to_shopping_cart,
    recipe_by_author
):
    RESPONSE_DATA = {
        "id": recipe_by_author.id,
        "name": NAME_RECIPE,
        "cooking_time": COOKING_TIME
    }
    response = user.post(post_delete_recipe_to_shopping_cart)
    assert response.status_code == status_post
    response_data = response.json()
    assert response_data['id'] == RESPONSE_DATA['id']
    assert response_data['name'] == RESPONSE_DATA['name']
    assert response_data['cooking_time'] == RESPONSE_DATA['cooking_time']
    assert settings.MEDIA_URL in response_data['image']

    response = user.delete(post_delete_recipe_to_shopping_cart)
    assert response.status_code == status_delete
