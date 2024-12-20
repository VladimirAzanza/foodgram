from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import TagSerializer
from tags.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
