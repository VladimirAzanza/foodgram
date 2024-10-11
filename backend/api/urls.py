from django.urls import include, path

from .views import CustomUserViewSet


app_name = 'api_v1'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
