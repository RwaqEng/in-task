
from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)

# يمكنك هنا تعريف الراوتات الخاصة بـ auth
# مثلاً:
@auth_blueprint.route('/login')
def login():
    return "Login Page"
