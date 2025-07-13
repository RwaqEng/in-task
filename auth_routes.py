from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# يمكنك هنا تعريف الراوتات الخاصة بـ auth
# مثلاً:
@auth_bp.route('/login')
def login():
    return "Login Page"
