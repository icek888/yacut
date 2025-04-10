from datetime import datetime

from . import db


class URLMap(db.Model):
    """Модель для хранения длинной и короткой ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
