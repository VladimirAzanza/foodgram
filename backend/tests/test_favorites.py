from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status_post, status_again_post, status_delete',
    (
        (
            lazy_fixture('author_client'),
            HTTPStatus.CREATED,
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.NO_CONTENT
        ),
        (
            lazy_fixture('not_author_client'),
            HTTPStatus.CREATED,
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.NO_CONTENT
        ),
        (
            lazy_fixture('client'),
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.UNAUTHORIZED
        )
    )
)
def test_subscribe(
    user,
    status_post,
    status_again_post,
    status_delete,
    post_delete_favorite_url
):
    response = user.post(post_delete_favorite_url)
    assert response.status_code == status_post
    response = user.post(post_delete_favorite_url)
    assert response.status_code == status_again_post
    response = user.delete(post_delete_favorite_url)
    assert response.status_code == status_delete
