from recipes.models import IngredientRecipe


def check_object_in_model(self, obj, model):
    user = self.context['request'].user
    return (
        user.is_authenticated and model.objects.filter(
            recipe=obj, author=user
        ).exists()
    )


def create_ingredient_recipe(instance, ingredients):
    for ingredient in ingredients:
        IngredientRecipe.objects.create(
            recipe=instance,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        )
