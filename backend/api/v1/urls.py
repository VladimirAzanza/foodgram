from django.urls import include, path

app_name = 'api_v1'

urlpatterns = [
    path('auth/', include(
        'djoser.urls.authtoken'
    )),
    path('users/', include(
        'api.v1.users.urls', namespace='users'
    )),
    path('tags/', include(
        'api.v1.tags.urls', namespace='tags'
    )),
    path('recipes/', include(
        'api.v1.recipes.urls', namespace='recipes'
    )),
    path('ingredients/', include(
        'api.v1.ingredients.urls', namespace='ingredients'
    )),
]
