from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
from django.db import models

from foodgram_backend.constants import (
    # AT_LEAST_ONE_INGREDIENT_MESSAGE,
    DEFAULT_COOKING_TIME,
    MAX_LENGTH_NAME_FIELD
)
from ingredients.models import Ingredient
from tags.models import Tag


User = get_user_model()


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientRecipe',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        null=False,
        blank=False
    )
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME_FIELD,
        null=False,
        blank=False
    )
    text = models.TextField(
        'Описание',
        null=False,
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=DEFAULT_COOKING_TIME
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        # if not self.ingredients.exists():
        # raise ValidationError(AT_LEAST_ONE_INGREDIENT_MESSAGE)

    @admin.display(description='Количество избранных')
    def count_favorite(self):
        return self.recipes_favorite_related.count()


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (
            f'{self.ingredient.name}-{self.amount} '
            f'{self.ingredient.measurement_unit} в {self.recipe.name}'
        )


class CommonFavoriteShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss"
    )

    class Meta:
        abstract = True


class Favorite(CommonFavoriteShoppingCart):
    class Meta(CommonFavoriteShoppingCart.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'author'],
                name='unique_favorite_author_recipe'
            )
        ]

    def __str__(self):
        return f'Избранное: {self.author}'


class ShoppingCart(CommonFavoriteShoppingCart):
    class Meta(CommonFavoriteShoppingCart.Meta):
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'author'],
                name='unique_cart_author_recipe'
            )
        ]

    def __str__(self):
        return f'Корзина покупок: {self.author}'
