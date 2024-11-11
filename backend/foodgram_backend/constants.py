# Constants for Tags
MAX_LENGTH_FIELD = 32
SLUG_FIELD_ERROR_TEXT = {
    'max_length': f'Слаг не может превышать {MAX_LENGTH_FIELD} символов.',
    'unique': 'Слаг должен быть уникальным.',
    'invalid': 'Введите действительный слаг (латиница, цифры, _ или -).'
}
SLUG_FIELD_HELP_TEXT = (
    f'Слаг не может превышать {MAX_LENGTH_FIELD} символов. '
    'Слаг должен быть уникальным. '
    'Введите действительный слаг (латиница, цифры, _ или -).'
)

# Constants for Recipes
MAX_LENGTH_NAME_FIELD = 256
DEFAULT_COOKING_TIME = 1
AT_LEAST_ONE_INGREDIENT_MESSAGE = (
    'Рецепт должен содержать хотя бы один ингредиент.'
)
MESSAGES = {
    'no_recipe': {'detail': 'Рецепт не найден'},
    'recipe_already_added': {'detail': 'Рецепт уже добавлен'},
    'recipe_deleted': {'detail': 'Рецепт успешно удален'},
    'no_shopping_cart': {'detail': 'Корзина пуста'}
}
RECIPE_INGREDIENT_NAME_PATH = 'recipe__ingredient_recipe__ingredient__name'
RECIPE_INGREDIENT_AMOUNT_PATH = 'recipe__ingredient_recipe__amount'
RECIPE_INGREDIENT_MEASUREMENT_UNIT_PATH = (
    'recipe__ingredient_recipe__ingredient__measurement_unit'
)
MIN_VALUE_FOR_COOKING_TIME = 1
MIN_VALUE_FOR_AMOUNT = 1
ADD_TAGS_MESSAGE = 'Добавьте теги'
DO_NOT_REPEAT_TAGS_MESSAGE = 'Теги не должны повторяться.'
ADD_INGREDIENTS_MESSAGE = 'Добавьте ингредиенты'
DO_NOT_REPEAT_INGREDIENTS_MESSAGE = 'Ингредиенты не должны повторяться.'

# Constants for Ingredients
MAX_LENGTH_NAME_FIELD = 128
MAX_LENGTH_MEASUREMENT_FIELD = 64
MEASUREMENT_UNITS = [
    ('г', 'Грамм'),
    ('кг', 'Килорамм'),
    ('л', 'Литр'),
    ('мл', 'Миллитр'),
    ('шт.', 'шт.'),
    ('банка', 'банка'),
    ('ст. л.', 'ст. л.'),
    ('ч. л.', 'ч. л.'),
    ('капля', 'капля'),
    ('стакан', 'стакан'),
    ('щепотка', 'щепотка'),
    ('батон', 'батон')
]

# Constants for Users
MAX_CHAR_LENGTH = 150
CANNOT_SUBSCRIBE_TO_YOURSELF_MESSAGE = (
    'Вы не можете быть своим собственным подписдчиком.'
)
CANNOT_SUBSCRIBE_TO_YOURSELF = {
    'detail': 'Вы не можете быть своим собственным подписдчиком.'
}
ALREADY_SUBSCRIBED = {
    'detail': 'Уже подписан на пользователя'
}
NO_SUBSCRIPTION = {
    'detail': 'Вы не подписан на пользователя'
}
PROHIBITED_USERNAMES = [
    'me', 'admin', 'staff', 'superuser', 'moderator'
]
PROHIBITED_USERNAME_MESSAGE = (
    'Вы не можете использовать это имя пользователя. Это недопустимо. '
    'Пожалуйста, проверьте имя пользователя. '
)
PROHIBITED_FIRST_NAME_MESSAGE = (
    'Вы не можете использовать это имя. Это недопустимо. '
    'Пожалуйста, проверьте имя. '
)
PROHIBITED_LAST_NAME_MESSAGE = (
    'Вы не можете использовать это имя для фамилии. Это недопустимо. '
    'Пожалуйста, проверьте фамилию. '
)
