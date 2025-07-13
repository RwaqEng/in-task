from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from extensions import db, migrate
from auth_routes import auth_bp
from models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

        if not User.query.first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('adminpass'),
                full_name='Admin User',
                phone_number='0500000000',
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()

    return app
