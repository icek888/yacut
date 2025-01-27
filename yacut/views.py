import re

from flask import (
    render_template, request, flash, redirect, url_for
)

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import generate_unique_short


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if request.method == 'POST':
        original = request.form.get('original_link', '')
        custom_id = request.form.get('custom_id', '')

        if not original:
            flash('Поле "Длинная ссылка" обязательно для заполнения.')
            return render_template('index.html', form=form), 200

        if custom_id:
            if len(custom_id) > 16 or not re.match(r'^[A-Za-z0-9]+$',
                                                   custom_id):
                form.custom_id.errors = [
                    'Указано недопустимое имя для короткой ссылки'
                ]
                return render_template('index.html', form=form), 200

            if URLMap.query.filter_by(short=custom_id).first():
                form.custom_id.errors = [
                    'Предложенный вариант короткой ссылки уже существует.'
                ]
                return render_template('index.html', form=form), 200

            short = custom_id
        else:
            short = generate_unique_short()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        # Генерируем полный URL, чтобы отображать его пользователю
        short_link = url_for('redirect_short', short_id=short, _external=True)

        return render_template('index.html',
                               form=form, short_link=short_link), 200

    return render_template('index.html', form=form), 200


@app.route('/<string:short_id>')
def redirect_short(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original, code=302)
