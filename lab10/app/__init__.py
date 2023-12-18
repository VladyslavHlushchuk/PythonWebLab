from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name: str):
    # Construct the core application.
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Imports
        from app.todo.views import todo
        from .portfolio.views import portfolio
        from .authentication.views import auth
        from .infos.views import infos
        app.register_blueprint(todo)
        app.register_blueprint(portfolio)
        app.register_blueprint(auth)
        app.register_blueprint(infos)

        from app import views

        return app
