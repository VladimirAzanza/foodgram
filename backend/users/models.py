from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'Имя', max_length=150, blank=False, null=False
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True, null=False
    )
    email = models.EmailField(
        'Адрес электронной почты', blank=True, null=False
    )
    avatar = models.ImageField(
        upload_to='users/', null=True, blank=True
    )
    is_subscribed = models.BooleanField(default=False)
