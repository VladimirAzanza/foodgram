from django.contrib import admin

from recipes.models import Recipe, ShoppingCart


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name'
    )
    search_fields = (
        'id',
        'author__username',
        'name',
    )
    list_filter = (
        'author',
        'tags__slug'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'author'
    )
    search_fields = (
        'id',
        'recipe',
        'author'
    )
    list_filter = (
        'author',
        'recipe'
    )
