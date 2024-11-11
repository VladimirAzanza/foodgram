from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilters(filters.FilterSet):
    is_favorited = filters.NumberFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.BaseInFilter(
        method='filter_tags'
    )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(recipes_favorites__author=user)
        elif value == 0:
            return queryset.exclude(recipes_favorites__author=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(recipes_shoppingcarts__author=user)
        elif value == 0:
            return queryset.exclude(recipes_shoppingcarts__author=user)
        return queryset

    def filter_tags(self, queryset, name, value):
        return queryset.filter(
            tags__slug__in=self.request.query_params.getlist('tags')
        )

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags')