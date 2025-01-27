import random
import string


def get_unique_short_id(length=6):
    """Генерирует короткий идентификатор (по умолчанию 6 символов)."""
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(chars, k=length))
