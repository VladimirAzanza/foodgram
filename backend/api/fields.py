import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import Subscription

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def get_boolean_if_favorited_or_in_cart(self, obj, model):
    user = self.context['request'].user
    if user.is_authenticated:
        return model.objects.filter(
            recipe=obj, author=user
        ).exists()
    return False


def get_boolean_if_user_is_subscribed(user, following):
    if user.is_authenticated:
        if Subscription.objects.filter(
            user=user, following=following
        ):
            return True
        else:
            return False
    return False
