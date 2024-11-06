from django.db import models
from foodgram_backend.constants import (
    MAX_LENGTH_FIELD,
    SLUG_FIELD_ERROR_TEXT,
    SLUG_FIELD_HELP_TEXT
)


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_FIELD,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=MAX_LENGTH_FIELD,
        unique=True,
        help_text=SLUG_FIELD_HELP_TEXT,
        error_messages=SLUG_FIELD_ERROR_TEXT
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.slug
