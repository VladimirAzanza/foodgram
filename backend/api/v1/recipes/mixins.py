from rest_framework import status
from rest_framework.response import Response

from foodgram_backend.constants import (
    NO_RECIPE,
    RECIPE_ALREADY_ADDED,
    RECIPE_DELETED
)


def post_recipe(model, serializer, recipe, author):
    data, created = model.objects.get_or_create(
        recipe=recipe, author=author
    )
    if created:
        serializer = serializer(data).data
        return Response(
            serializer, status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            RECIPE_ALREADY_ADDED,
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_recipe(model, recipe, author):
    data = model.objects.filter(
        recipe=recipe, author=author
    )
    if data:
        data.delete()
        return Response(
            RECIPE_DELETED,
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        NO_RECIPE,
        status=status.HTTP_400_BAD_REQUEST
    )
