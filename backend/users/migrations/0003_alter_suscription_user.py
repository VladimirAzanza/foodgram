# Generated by Django 4.2.16 on 2024-10-22 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_is_subscribed_suscription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]