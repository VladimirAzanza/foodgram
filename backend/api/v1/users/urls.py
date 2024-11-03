from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CurrentUserAvatar, CustomUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('me/avatar/', CurrentUserAvatar.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
]
