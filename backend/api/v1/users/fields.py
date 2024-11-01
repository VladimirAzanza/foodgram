from rest_framework import serializers

from users.models import Subscription

from .constants import PROHIBITED_FIELD_MESSAGE, PROHIBITED_USERNAMES


def get_boolean_if_user_is_subscribed(user, following):
    if user.is_authenticated:
        if Subscription.objects.filter(
            user=user, following=following
        ):
            return True
        else:
            return False
    return False


def get_profanities_list(file_path):
    with open(file_path, 'r') as file:
        return tuple(word.strip().lower() for word in file)


def validate_field(field):
    english_profanities = get_profanities_list(
        'api/v1/users/data/profanities/en.txt'
    )
    russian_profanities = get_profanities_list(
        'api/v1/users/data/profanities/ru.txt'
    )
    field_lower = field.lower()
    if (
        field_lower in english_profanities
        or field_lower in russian_profanities
        or field_lower in PROHIBITED_USERNAMES
    ):
        raise serializers.ValidationError(PROHIBITED_FIELD_MESSAGE)
