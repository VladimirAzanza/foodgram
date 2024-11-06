from users.models import Subscription


def is_user_subscribed(user, following):
    return (
        user.is_authenticated and Subscription.objects.filter(
            user=user, following=following
        ).exists()
    )
