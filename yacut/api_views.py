import re

from flask import request, jsonify

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400

    if 'url' not in data:
        return jsonify({'message': '"url" является обязательным полем!'}), 400

    original = data['url']
    custom_id = data.get('custom_id')

    if not custom_id:
        short = _generate_unique_short()
    else:
        if len(custom_id) > 16:
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), 400

        if not re.match(r'^[A-Za-z0-9]+$', custom_id):
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), 400

        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify({
                'message': 'Предложенный вариант '
                'короткой ссылки уже существует.'
            }), 400

        short = custom_id

    url_map = URLMap(original=original, short=short)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': f'http://localhost/{url_map.short}'
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({'url': url_map.original}), 200


def _generate_unique_short():
    short = get_unique_short_id()
    while URLMap.query.filter_by(short=short).first():
        short = get_unique_short_id()
    return short
