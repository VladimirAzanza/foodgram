# Generated by Django 4.2.16 on 2024-10-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_alter_tag_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(error_messages='Введите допустимый "слаг", состоящий из латинских букв, букв, цифр, подчеркиваний или дефисов.', help_text='Введите допустимый "слаг", состоящий из латинских букв, букв, цифр, подчеркиваний или дефисов.', max_length=32, unique=True),
        ),
    ]