from users.models import Subscription


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
