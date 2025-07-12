from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# تصحيح مسارات الاستيراد لتعمل مع بنية rivaq_fixed/
from rivaq_fixed.blueprints.users import User  # تم تصحيح المسار

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///rivaq.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "rivaq-secret-key-2024-very-secure")
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة.'
    login_manager.login_message_category = 'info'

    # Import models after db initialization - تصحيح مسارات الاستيراد
    from rivaq_fixed.models import User, Task, Meeting, MeetingOutput
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints - تصحيح مسارات الاستيراد
    from rivaq_fixed.auth import auth_bp
    from rivaq_fixed.api import api_bp
    from rivaq_fixed.dashboard import dashboard_bp
    from rivaq_fixed.users import users_bp
    from rivaq_fixed.tasks import tasks_bp
    from rivaq_fixed.meetings import meetings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(meetings_bp, url_prefix='/meetings')
    
    # Create tables and initialize database
    with app.app_context():
        db.create_all()
        # Initialize database with sample data if empty
        if not User.query.first():
            from rivaq_fixed.init_db import init_database
            init_database(app, db)

    return app

# إنشاء instance للتطبيق للاستخدام مع gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

