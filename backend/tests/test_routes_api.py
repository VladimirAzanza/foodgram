from http import HTTPStatus

from django.urls import reverse
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'api_v1:users-list',
        'api_v1:tag-list',
        'api_v1:recipe-list',
        'api_v1:ingredient-list'
    )
)
def test_get_list_routes_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_get_my_user(admin_client):
    url = reverse('api_v1:current_user')
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK