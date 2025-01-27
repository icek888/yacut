from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length, Optional


class URLForm(FlaskForm):
    """Форма для ввода длинной ссылки"""
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректный URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=16, message='Максимум 16 символов'),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
