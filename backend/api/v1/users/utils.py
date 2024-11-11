from foodgram_backend.constants import PROHIBITED_USERNAMES
from users.models import Subscription


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


def get_subscriptions_data(
        user_profile,
        subscription_serializer,
        model,
        recipes_to_subscriptions_serializer,
        recipes_limit=None
):
    serializer_data = []
    for information in user_profile:
        serializer = subscription_serializer(information).data
        if recipes_limit:
            recipes = model.objects.filter(author=information.following)
            recipes = recipes[:int(recipes_limit)]
            serializer['recipes'] = recipes_to_subscriptions_serializer(
                recipes, many=True
            ).data
        serializer_data.append(serializer)
    return serializer_data


def is_user_subscribed(user, following):
    return (
        user.is_authenticated and Subscription.objects.filter(
            user=user, following=following
        ).exists()
    )
