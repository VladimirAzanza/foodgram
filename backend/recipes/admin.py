from django.contrib import admin

from recipes.models import Favorite, IngredientRecipe, Recipe, ShoppingCart


class IngredientInLine(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInLine,
    )
    filter_horizontal = (
        'tags',
    )
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'count_favorite'
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

    @admin.display(description='Количество избранных')
    def count_favorite(self, obj):
        return obj.recipes_favorite_related.count()


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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
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
