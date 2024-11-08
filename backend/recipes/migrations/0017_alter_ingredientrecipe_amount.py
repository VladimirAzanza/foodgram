# Generated by Django 4.2.16 on 2024-11-07 09:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]