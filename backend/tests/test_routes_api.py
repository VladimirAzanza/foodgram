from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        lazy_fixture('users_list_url'),
        lazy_fixture('tag_list_url'),
        lazy_fixture('recipe_list_url'),
        lazy_fixture('ingredient_list_url')
    )
)
def test_get_list_routes_availability_for_anonymous_user(client, name):
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        lazy_fixture('users_me_url'),
        lazy_fixture('not_author_user_url')
    )
)
def test_get_user_for_auth_user(author_client, name):
    response = author_client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        lazy_fixture('get_ingredient'),
        lazy_fixture('get_tag'),
        lazy_fixture('get_recipe')
    )
)
def test_get_detail(client, name):
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK
