from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import pytest

from .constants import(
    AUTHOR_USERNAME,
    AUTHOR_FIRST_NAME,
    AUTHOR_LAST_NAME,
    EMAIL_AUTHOR,
    EMAIL_NOT_AUTHOR,
    NOT_AUTHOR_USERNAME,
    NOT_AUTHOR_FIRST_NAME,
    NOT_AUTHOR_LAST_NAME,
    PASSWORD
)


@pytest.fixture
def author(django_user_model):
    user = django_user_model.objects.create(
        username=AUTHOR_USERNAME
    )
    Token.objects.create(user=user)
    return user


@pytest.fixture
def not_author(django_user_model):
    user = django_user_model.objects.create(
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