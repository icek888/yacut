import re

from flask import render_template, request, flash, redirect

from .forms import URLForm
from .models import db, URLMap
from .utils import get_unique_short_id
from . import app


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
            if len(custom_id) > 16 or not re.match(
                    r'^[A-Za-z0-9]+$', custom_id):
                form.custom_id.errors = [
                    'Указано недопустимое имя для короткой ссылки']
                return render_template('index.html', form=form), 200

            if URLMap.query.filter_by(short=custom_id).first():
                form.custom_id.errors = [
                    'Предложенный вариант короткой ссылки уже существует.']
                return render_template('index.html', form=form), 200

            short = custom_id
        else:
            short = _generate_unique_short()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        return render_template('index.html', form=form, short=short), 200

    return render_template('index.html', form=form), 200


@app.route('/<string:short_id>')
def redirect_short(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original, code=302)


def _generate_unique_short():
    short = get_unique_short_id()
    while URLMap.query.filter_by(short=short).first():
        short = get_unique_short_id()
    return short
