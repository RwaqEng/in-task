from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

# Import the User model from the main models file
from rivaq_fixed.models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
def users_home():
    return "صفحة المستخدمين (قيد التطوير)"

