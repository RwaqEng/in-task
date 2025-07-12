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
    
    # Apply filters
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    
    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('tasks.html', tasks=tasks, 
                         status_filter=status_filter, 
                         priority_filter=priority_filter)

@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if not current_user.has_permission('create_tasks'):
        flash('غير مصرح لك بإنشاء مهام', 'error')
        return redirect(url_for('tasks.tasks_list'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        priority = request.form.get('priority', 'متوسطة')
        due_date = request.form.get('due_date')
        
        if not title:
            flash('يرجى إدخال عنوان المهمة', 'error')
            return render_template('add_task.html')
        
        new_task = Task(
            title=title,
            description=description,
            assigned_to=int(assigned_to) if assigned_to else None,
            created_by=current_user.id,
            priority=priority,
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        flash('تم إنشاء المهمة بنجاح', 'success')
        return redirect(url_for('tasks.tasks_list'))
    
    users = User.query.all()
    return render_template('add_task.html', users=users)

@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Check permissions
    if not (current_user.has_permission('edit_tasks') or 
            task.assigned_to == current_user.id or 
            task.created_by == current_user.id):
        flash('غير مصرح لك بتعديل هذه المهمة', 'error')
        return redirect(url_for('tasks.tasks_list'))
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.priority = request.form.get('priority')
        task.status = request.form.get('status')
        task.progress = int(request.form.get('progress', 0))
        
        assigned_to = request.form.get('assigned_to')
        task.assigned_to = int(assigned_to) if assigned_to else None
        
        due_date = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
        
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('تم تحديث المهمة بنجاح', 'success')
        return redirect(url_for('tasks.tasks_list'))
    
    users = User.query.all()
    return render_template('edit_task.html', task=task, users=users)

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if not (current_user.has_permission('delete_tasks') or task.created_by == current_user.id):
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بحذف هذه المهمة'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'تم حذف المهمة بنجاح'})

@tasks_bp.route('/update-progress/<int:task_id>', methods=['POST'])
@login_required
def update_progress(task_id):
    task = Task.query.get_or_404(task_id)
    
    if not (task.assigned_to == current_user.id or 
            task.created_by == current_user.id or 
            current_user.has_permission('edit_tasks')):
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بتحديث هذه المهمة'}), 403
    
    progress = request.json.get('progress', 0)
    task.progress = max(0, min(100, int(progress)))
    
    # Auto-update status based on progress
    if task.progress == 0:
        task.status = 'جديدة'
    elif task.progress == 100:
        task.status = 'مكتملة'
    else:
        task.status = 'قيد التنفيذ'
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'تم تحديث تقدم المهمة'})

