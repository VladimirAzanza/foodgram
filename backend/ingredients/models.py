from django.db import models

from foodgram_backend.constants import (
    MAX_LENGTH_MEASUREMENT_FIELD,
    MAX_LENGTH_NAME_FIELD,
    MEASUREMENT_UNITS
)


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME_FIELD
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LENGTH_MEASUREMENT_FIELD,
        choices=MEASUREMENT_UNITS
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name
