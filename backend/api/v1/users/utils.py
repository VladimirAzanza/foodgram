from rest_framework import serializers

from .constants import PROHIBITED_USERNAMES


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
        return False
    return True
