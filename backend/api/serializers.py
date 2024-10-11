from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'password'
        )
        read_only_fields = ('avatar', 'is_subscribed')
        extra_kwargs = {
            'password': {
                'write_only': True, 'required': True, 'allow_blank': False
            },
            'email': {
                'required': True, 'allow_blank': False
            },
            'username': {
                'required': True, 'allow_blank': False
            },
            'first_name': {
                'required': True, 'allow_blank': False
            },
            'last_name': {
                'required': True, 'allow_blank': False
            },
        }
