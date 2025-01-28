import re
from http import HTTPStatus

from flask import request, jsonify

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id
from .error_handlers import APIError


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """
    Создание новой короткой ссылки (POST /api/id/).
    Возвращает JSON с полями:
      - 'url': исходная ссылка
      - 'short_link': короткая ссылка
    """
    data = request.get_json(silent=True)
    if data is None:
        raise APIError('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)

    if 'url' not in data:
        raise APIError('"url" является обязательным полем!',
                       HTTPStatus.BAD_REQUEST)

    original = data['url']
    custom_id = data.get('custom_id')

    if custom_id is None or custom_id == '':
        short = _generate_unique_short()
    else:
        if len(custom_id) > 16:
            raise APIError(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )

        if not re.match(r'^[A-Za-z0-9]+$', custom_id):
            raise APIError(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )

        existing_url = URLMap.query.filter_by(short=custom_id).first()
        if existing_url is not None:
            raise APIError(
                'Предложенный вариант короткой ссылки уже существует.',
                HTTPStatus.BAD_REQUEST
            )
        short = custom_id

    url_map = URLMap(original=original, short=short)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': f'{request.host_url}{url_map.short}'
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Получение исходной ссылки по короткому идентификатору.
    (GET /api/id/<short_id>/)
    """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise APIError('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_map.original}), HTTPStatus.OK


def _generate_unique_short():
    """
    Генерация случайного короткого идентификатора,
    который не конфликтует с уже существующими в БД.
    """
    short = get_unique_short_id()
    while URLMap.query.filter_by(short=short).first() is not None:
        short = get_unique_short_id()
    return short
