from rest_framework import status
from rest_framework.response import Response

from foodgram_backend.constants import MESSAGES


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
            MESSAGES['recipe_already_added'],
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_recipe(model, recipe, author):
    data = model.objects.filter(
        recipe=recipe, author=author
    )
    if data:
        data.delete()
        return Response(
            MESSAGES['recipe_deleted'],
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        MESSAGES['no_recipe'],
        status=status.HTTP_400_BAD_REQUEST
    )
