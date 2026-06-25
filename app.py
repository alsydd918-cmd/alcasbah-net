import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'production')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول أولاً'
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.users import users_bp
    from app.routes.towers import towers_bp
    from app.routes.tasks import tasks_bp
    from app.routes.mikrotik import mikrotik_bp
    from app.routes.reports import reports_bp
    from app.routes.settings import settings_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(towers_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(mikrotik_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
    
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'الصفحة غير موجودة'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return {'error': 'خطأ في الخادم'}, 500
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
