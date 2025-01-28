import re
from http import HTTPStatus

from flask import render_template, request, flash, redirect, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Главная страница: форма для длинной ссылки и опционального custom_id.
    При POST сохраняет запись в БД и выводит короткую ссылку.
    """
    form = URLForm()
    if request.method == 'POST':
        original = request.form.get('original_link', '')
        custom_id = request.form.get('custom_id', '')

        if not original:
            flash('Поле "Длинная ссылка" обязательно для заполнения.')
            return render_template('index.html', form=form), HTTPStatus.OK

        if custom_id:
            if (
                len(custom_id) > 16
                or not re.match(r'^[A-Za-z0-9]+$', custom_id)
            ):
                form.custom_id.errors = [
                    'Указано недопустимое имя для короткой ссылки'
                ]
                return render_template('index.html', form=form), HTTPStatus.OK

            existing_url = URLMap.query.filter_by(short=custom_id).first()
            if existing_url is not None:
                form.custom_id.errors = [
                    'Предложенный вариант короткой ссылки уже существует.'
                ]
                return render_template('index.html', form=form), HTTPStatus.OK

            short = custom_id
        else:
            short = _generate_unique_short()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        short_link = url_for('redirect_short', short_id=short, _external=True)
        return render_template('index.html',
                               form=form, short_link=short_link), HTTPStatus.OK

    return render_template('index.html', form=form), HTTPStatus.OK


@app.route('/<string:short_id>')
def redirect_short(short_id):
    """
    Редирект по короткой ссылке.
    """
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original, code=HTTPStatus.FOUND)


def _generate_unique_short():
    """
    Генерирует короткий идентификатор, проверяя коллизии в БД.
    """
    short = get_unique_short_id()
    while URLMap.query.filter_by(short=short).first() is not None:
        short = get_unique_short_id()
    return short
