from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

app_name = 'ingredients'

router = DefaultRouter()
router.register('', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
