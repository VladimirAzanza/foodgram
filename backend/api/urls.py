from django.urls import include, path


app_name = 'api_v1'

urlpatterns = [
    path('users/', include('djosers.urls')),
    path('users/auth', include('djoser.urls.authtoken')),
]
