from django.db import models

from .constants import MAX_LENGTH_FIELD, SLUG_FIELD_HELP_TEXT


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_FIELD
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_FIELD,
        help_text=SLUG_FIELD_HELP_TEXT
    )
