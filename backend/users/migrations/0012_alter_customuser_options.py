# Generated by Django 4.2.16 on 2024-11-07 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('username',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]