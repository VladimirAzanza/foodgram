from django.contrib.auth import get_user_model
from django.db import models

from .constants import DEFAULT_COOKING_TIME, MAX_LENGTH_NAME_FIELD
from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag, related_name='recipes'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/', null=True, blank=True
    )
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_FIELD,
        null=True
    )
    text = models.TextField(
        null=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=DEFAULT_COOKING_TIME
    )
