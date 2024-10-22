from django.contrib import admin

from ingredients.models import Ingredient
from recipes.models import Recipe, ShoppingCart
from tags.models import Tag
from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'username',
        'is_staff',
        'date_joined'
    )
    search_fields = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_editable = (
        'is_staff',
    )
    list_filter = (
        'is_staff',
        'date_joined'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = (
        'name',
        'slug',
    )
    search_fields = (
        'id',
        'name',
        'slug'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name'
    )
    search_fields = (
        'id',
        'author',
        'name'
    )
    list_filter = (
        'author',
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


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = (
        'id',
        'name'
    )
    list_filter = (
        'name',
    )
