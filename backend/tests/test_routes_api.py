from http import HTTPStatus

from django.urls import reverse
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    [
        pytest.lazy_fixture('users_list_url'),
        pytest.lazy_fixture('tag_list_url'),
        pytest.lazy_fixture('recipe_list_url'),
        pytest.lazy_fixture('ingredient_list_url')
    ]
)
def test_get_list_routes_availability_for_anonymous_user(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'api_v1:users-me',
    )
)
def test_get_user(author_client, name):
    url = reverse(name)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK
