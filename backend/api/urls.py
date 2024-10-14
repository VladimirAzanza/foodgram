from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CurrentUserAvatar,
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet
)


app_name = 'api_v1'
router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tag')
router_v1.register('recipes', RecipeViewSet, basename='recipe')
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', CurrentUserAvatar.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    path('', include(router_v1.urls)),
]
