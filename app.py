
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from models import User, Task, Meeting, MeetingOutput
from users import users_bp
from tasks import tasks_bp
from dashboard import dashboard_bp
from meetings import meetings_bp
from api import api_bp
from auth_routes import auth_bp  # ✅ التعديل هنا

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(meetings_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)  # ✅ تأكدنا من تسجيل البلوبرنت

    with app.app_context():
        db.create_all()
        if not User.query.first():
            admin_user = User(
                username='admin',
                full_name='Admin User',
                email='admin@example.com',
                phone_number='1234567890',
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
# Force rebuild
