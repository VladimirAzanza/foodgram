MAX_LENGTH_FIELD = 32
SLUG_FIELD_ERROR_TEXT = {
    'max_length': 'Slug не может превышать {max_length} символов.',
    'unique': 'Slug должен быть уникальным.',
    'invalid': 'Введите действительный slug (латиница, цифры, _ или -).'
}
SLUG_FIELD_HELP_TEXT = (
    f'Slug не может превышать {MAX_LENGTH_FIELD} символов.'
    'Slug должен быть уникальным.'
    'Введите действительный slug (латиница, цифры, _ или -).'
)
