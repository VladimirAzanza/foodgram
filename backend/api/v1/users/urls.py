from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, CurrentUserAvatar

router = DefaultRouter()
router.register('', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('me/avatar/', CurrentUserAvatar.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
]
