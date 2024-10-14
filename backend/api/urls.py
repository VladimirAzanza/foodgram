from django.urls import include, path

from .views import CurrentUserAvatar


app_name = 'api_v1'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', CurrentUserAvatar.as_view({
        'put': 'update',
        'delete': 'destroy'
    }))
]
