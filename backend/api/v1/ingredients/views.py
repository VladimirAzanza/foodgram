from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from ingredients.models import Ingredient

from .serializers import IngredientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
