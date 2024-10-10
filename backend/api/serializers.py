from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
            'password': {'write_only': True}
        }
