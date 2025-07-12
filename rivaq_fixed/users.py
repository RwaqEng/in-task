from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from rivaq_fixed.extensions import db
from rivaq_fixed.models import User
import json

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
@login_required
def users_list():
    if not current_user.has_permission('view_users'):
        flash('غير مصرح لك بعرض المستخدمين', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('users.html', users=users)

@users_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.has_permission('manage_users'):
        flash('غير مصرح لك بإضافة مستخدمين', 'error')
        return redirect(url_for('users.users_list'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        position = request.form.get('position')
        department = request.form.get('department')
        manager_id = request.form.get('manager_id')
        
        if not all([name, email, password, position, department]):
            flash('يرجى ملء جميع الحقول المطلوبة', 'error')
            return render_template('add_user.html')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('البريد الإلكتروني مستخدم بالفعل', 'error')
            return render_template('add_user.html')
        
        # Create new user
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            position=position,
            department=department,
            manager_id=int(manager_id) if manager_id else None
        )
        
        # Set default permissions
        default_permissions = ['view_tasks', 'edit_tasks']
        new_user.set_permissions(default_permissions)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('تم إضافة المستخدم بنجاح', 'success')
        return redirect(url_for('users.users_list'))
    
    # Get managers for dropdown
    managers = User.query.all()
    return render_template('add_user.html', managers=managers)

@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.has_permission('manage_users'):
        flash('غير مصرح لك بتعديل المستخدمين', 'error')
        return redirect(url_for('users.users_list'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.position = request.form.get('position')
        user.department = request.form.get('department')
        manager_id = request.form.get('manager_id')
        user.manager_id = int(manager_id) if manager_id else None
        
        # Update password if provided
        new_password = request.form.get('password')
        if new_password:
            user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('تم تحديث بيانات المستخدم بنجاح', 'success')
        return redirect(url_for('users.users_list'))
    
    managers = User.query.filter(User.id != user_id).all()
    return render_template('edit_user.html', user=user, managers=managers)

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.has_permission('manage_users'):
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بحذف المستخدمين'}), 403
    
    if user_id == current_user.id:
        return jsonify({'status': 'error', 'message': 'لا يمكنك حذف حسابك الخاص'}), 400
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'تم حذف المستخدم بنجاح'})

