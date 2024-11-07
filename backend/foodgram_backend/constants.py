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
NO_RECIPE = {
    "detail": "Рецепт не найден"
}
RECIPE_ALREADY_ADDED = {
    "detail": "Рецепт уже добавлен"
}
RECIPE_DELETED = {
    "detail": "Рецепт успешно удален"
}
NO_SHOPPING_CART = {
    "detail": "Корзина пуста"
}
MIN_VALUE_FOR_COOKING_TIME = 1
MIN_VALUE_FOR_AMOUNT = 1

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
CANNOT_SUBSCRIBE_TO_YOURSELF = {
    "detail": "Вы не можете быть своим собственным подписдчиком."
}
ALREADY_SUBSCRIBED = {
    "detail": "Уже подписан на пользователя"
}
NO_SUBSCRIPTION = {
    "detail": "Вы не подписан на пользователя"
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
