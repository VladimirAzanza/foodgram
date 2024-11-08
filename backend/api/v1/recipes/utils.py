def check_object_in_model(self, obj, model):
    user = self.context['request'].user
    return (
        user.is_authenticated and model.objects.filter(
            recipe=obj, author=user
        ).exists()
    )
