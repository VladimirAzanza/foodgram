def get_boolean_if_favorited_or_in_cart(self, obj, model):
    user = self.context['request'].user
    if user.is_authenticated:
        return model.objects.filter(
            recipe=obj, author=user
        ).exists()
    return False
