def check_object_in_model(self, obj, model):
    user = self.context['request'].user
    if user.is_authenticated:
        return model.objects.filter(
            recipe=obj, author=user
        ).exists()
    return False
