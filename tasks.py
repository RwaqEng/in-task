from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def tasks_list():
    if not current_user.has_permission('view_tasks'):
        flash('غير مصرح لك بعرض المهام', 'error')
        return redirect(url_for('dashboard.dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page = 20
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')

    query = Task.query

    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)

    tasks = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('tasks/list.html', tasks=tasks, status_filter=status_filter, priority_filter=priority_filter)

@tasks_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    if not current_user.has_permission('create_task'):
        return jsonify({'error': 'Unauthorized'}), 403

    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')

    if not title:
        return jsonify({'error': 'العنوان مطلوب'}), 400

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('tasks.tasks_list'))

@tasks_bp.route('/update/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not current_user.has_permission('edit_task') and task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    task.title = request.form.get('title', task.title)
    task.description = request.form.get('description', task.description)
    task.priority = request.form.get('priority', task.priority)
    task.status = request.form.get('status', task.status)

    db.session.commit()
    return redirect(url_for('tasks.tasks_list'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not current_user.has_permission('delete_task') and task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks.tasks_list'))
