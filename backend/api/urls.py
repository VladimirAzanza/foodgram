from django.urls import include, path

from .views import CustomUserViewSet


app_name = 'api_v1'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

'''
    path('users/', CustomUserViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('users/<int:pk>/', CustomUserViewSet.as_view({
        'get': 'retrieve'
    })),
'''
