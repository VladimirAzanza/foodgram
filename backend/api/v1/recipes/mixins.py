from rest_framework import status
from rest_framework.response import Response

from api.v1.recipes.constants import (
    NO_RECIPE, RECIPE_ALREADY_ADDED, RECIPE_DELETED
)


def post_delete_recipe(self, request, model, serializer):
    recipe = self.get_object()
    if request.method == 'POST':
        data, data_created = model.objects.get_or_create(
            recipe=recipe, author=request.user
        )
        if data_created:
            response_data = serializer(data).data
            return Response(
                response_data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                RECIPE_ALREADY_ADDED,
                status=status.HTTP_400_BAD_REQUEST
            )
    if request.method == 'DELETE':
        data = model.objects.filter(
            recipe=recipe, author=self.request.user
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
