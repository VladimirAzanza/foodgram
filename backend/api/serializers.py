from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import ModelSerializer

User = get_user_model()


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
        )


class CreateCustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }


class CustomCurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )
        read_only_fields = (
            'id',
            'is_subscribed'
        )


class AvatarCurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)
