import random
import string

from .models import URLMap


def get_unique_short_id(length=6):
    """Генерирует короткий идентификатор (по умолчанию 6 символов)."""
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(chars, k=length))


def generate_unique_short():
    """Формирует уникальный short, проверяя коллизии в БД."""
    short = get_unique_short_id()
    while URLMap.query.filter_by(short=short).first():
        short = get_unique_short_id()
    return short
