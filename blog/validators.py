import re

from django.core.exceptions import ValidationError

from .constants import MAX_LENGTH_TITLE, MIN_LENGTH_TITLE


def validate_title(value: str) -> None:
    """
    Проверяет, что заголовок не короче 3 символов и не состоит только из чисел.
    """
    if not (MIN_LENGTH_TITLE <= len(value.strip()) <= MAX_LENGTH_TITLE):
        raise ValidationError(
            ('Заголовок должен быть не короче 3 и не длиннее 50 символов.')
        )
    if re.fullmatch(r'\d+', value.strip()):
        raise ValidationError(('Заголовок не может состоять только из чисел.'))
