from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

app.config.from_object('settings')

db.init_app(app)
migrate.init_app(app, db)

from . import views, api_views, error_handlers
