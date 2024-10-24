from django.contrib.auth import get_user_model
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
        'Адрес электронной почты', blank=True, null=False, unique=True,
    )
    avatar = models.ImageField(
        upload_to='users/', null=True, blank=True
    )


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]
