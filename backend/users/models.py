from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram_backend.constants import MAX_CHAR_LENGTH


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'Имя', max_length=MAX_CHAR_LENGTH,
    )
    last_name = models.CharField(
        'Фамилия', max_length=MAX_CHAR_LENGTH,
    )
    email = models.EmailField(
        'Адрес электронной почты', unique=True,
    )
    avatar = models.ImageField(
        'Аватар', upload_to='users/', null=True, blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name', 'password'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан на'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
