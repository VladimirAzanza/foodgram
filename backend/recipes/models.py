from django.contrib.auth import get_user_model
from django.db import models

from tags.models import Tag
from ingredients.models import Ingredient

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
