from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from extensions import db
from models import User, Task, Meeting, MeetingOutput
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Get dashboard statistics
    total_users = User.query.count()
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status='جديدة').count()
    in_progress_tasks = Task.query.filter_by(status='قيد التنفيذ').count()
    completed_tasks = Task.query.filter_by(status='مكتملة').count()
    total_meetings = Meeting.query.count()
    upcoming_meetings = Meeting.query.filter_by(status='مجدولة').count()
    
    # Get recent tasks
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    
    # Get upcoming meetings
    upcoming_meetings_list = Meeting.query.filter(
        Meeting.meeting_date >= datetime.now(),
        Meeting.status == 'مجدولة'
    ).order_by(Meeting.meeting_date.asc()).limit(5).all()
    
    # Get user's assigned tasks
    user_tasks = Task.query.filter_by(assigned_to=current_user.id).limit(5).all()
    
    stats = {
        'total_users': total_users,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'total_meetings': total_meetings,
        'upcoming_meetings': upcoming_meetings
    }
    
    return render_template('dashboard.html', 
                         stats=stats,
                         recent_tasks=recent_tasks,
                         upcoming_meetings=upcoming_meetings_list,
                         user_tasks=user_tasks)

@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@dashboard_bp.route('/reports')
@login_required
def reports():
    if not current_user.has_permission('view_reports'):
        return render_template('error.html', message='غير مصرح لك بعرض التقارير')
    
    return render_template('reports.html')

