from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CurrentUserAvatar, CustomUserViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet)
from django.http import HttpResponse
app_name = 'api_v1'
router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tag')
router_v1.register('recipes', RecipeViewSet, basename='recipe')
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', CurrentUserAvatar.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    path('', include(router_v1.urls)),
    path('list-urls/', lambda request: HttpResponse('<br>'.join(str(url) for url in router_v1.urls), content_type='text/html')),
]
