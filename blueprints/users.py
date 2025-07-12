from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from flask_login import login_required
from models import User  # ✅ استيراد مباشر من المسار الجديد
from extensions import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@users_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username and email:
            user.username = username
            user.email = email
            if password:
                user.password = generate_password_hash(password)
            db.session.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('users.users'))
        else:
            flash('Username and email are required.', 'danger')

    return render_template('edit_user.html', user=user)

