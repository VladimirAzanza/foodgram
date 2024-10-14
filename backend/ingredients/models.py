from django.db import models

from .constants import (
    MAX_LENGTH_MEASUREMENT_FIELD, MAX_LENGTH_NAME_FIELD, MEASUREMENT_UNITS
)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_FIELD
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_MEASUREMENT_FIELD,
        choices=MEASUREMENT_UNITS
    )