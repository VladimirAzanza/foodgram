from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/', null=True, blank=True
    )
    is_subscribed = models.BooleanField(default=False)
