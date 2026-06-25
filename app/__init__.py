from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='default'):
    """Application factory."""
    app = Flask(name)

    from config import config
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول لهذه الصفحة'
    login_manager.login_message_category = 'warning'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.mikrotik import mikrotik_bp
    from app.reports import reports_bp
    from app.settings import settings_bp
    from app.tasks import tasks_bp
    from app.towers import towers_bp
    from app.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(mikrotik_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(towers_bp)
    app.register_blueprint(users_bp)

    return app
