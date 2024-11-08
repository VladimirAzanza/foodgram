from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from api.v1.users.utils import validate_field
from foodgram_backend.constants import (
    CANNOT_SUBSCRIBE_TO_YOURSELF,
    MAX_CHAR_LENGTH,
    PROHIBITED_FIRST_NAME_MESSAGE,
    PROHIBITED_LAST_NAME_MESSAGE,
    PROHIBITED_USERNAME_MESSAGE
)


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
        'Аватар', upload_to='users/', null=True, blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name', 'password'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def clean(self):
        super().clean()
        if not validate_field(self.username):
            raise ValidationError(PROHIBITED_USERNAME_MESSAGE)
        if not validate_field(self.first_name):
            raise ValidationError(PROHIBITED_FIRST_NAME_MESSAGE)
        if not validate_field(self.last_name):
            raise ValidationError(PROHIBITED_LAST_NAME_MESSAGE)


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
        ordering = ('id',)

    def clean(self):
        super().clean()
        if self.user == self.following:
            raise ValidationError(CANNOT_SUBSCRIBE_TO_YOURSELF)

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
