from flask import Blueprint, jsonify, request
from flask_mail import Message
from flask_login import login_required, current_user
# تصحيح مسارات الاستيراد
from rivaq_fixed.extensions import db, mail
from rivaq_fixed.models import User, Task, Meeting, MeetingOutput

api_bp = Blueprint("api", __name__)

@api_bp.route("/send-test-email")
@login_required
def send_test_email():
    try:
        msg = Message(
            subject="Test Email from Rivaq System",
            sender="asala.alsaaf@rwaqeng.com",
            recipients=["asala.alsaaf@rwaqeng.com"],
            body="This is a test email sent from Flask Rivaq System!"
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}", "status": "error"}), 500

@api_bp.route("/users")
@login_required
def get_users():
    if not current_user.has_permission('view_users'):
        return jsonify({"message": "غير مصرح لك بعرض المستخدمين", "status": "error"}), 403
    
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'position': user.position,
            'department': user.department,
            'join_date': user.join_date.isoformat() if user.join_date else None
        })
    
    return jsonify({"users": users_data, "status": "success"})

@api_bp.route("/tasks")
@login_required
def get_tasks():
    if not current_user.has_permission('view_tasks'):
        return jsonify({"message": "غير مصرح لك بعرض المهام", "status": "error"}), 403
    
    tasks = Task.query.all()
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'progress': task.progress,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'assignee': task.assignee.name if task.assignee else None,
            'creator': task.creator.name if task.creator else None
        })
    
    return jsonify({"tasks": tasks_data, "status": "success"})

@api_bp.route("/meetings")
@login_required
def get_meetings():
    if not current_user.has_permission('view_meetings'):
        return jsonify({"message": "غير مصرح لك بعرض الاجتماعات", "status": "error"}), 403
    
    meetings = Meeting.query.all()
    meetings_data = []
    for meeting in meetings:
        meetings_data.append({
            'id': meeting.id,
            'title': meeting.title,
            'description': meeting.description,
            'meeting_date': meeting.meeting_date.isoformat() if meeting.meeting_date else None,
            'location': meeting.location,
            'status': meeting.status,
            'organizer': meeting.organizer.name if meeting.organizer else None
        })
    
    return jsonify({"meetings": meetings_data, "status": "success"})

@api_bp.route("/dashboard-stats")
@login_required
def get_dashboard_stats():
    stats = {
        'total_users': User.query.count(),
        'total_tasks': Task.query.count(),
        'pending_tasks': Task.query.filter_by(status='جديدة').count(),
        'in_progress_tasks': Task.query.filter_by(status='قيد التنفيذ').count(),
        'completed_tasks': Task.query.filter_by(status='مكتملة').count(),
        'total_meetings': Meeting.query.count(),
        'upcoming_meetings': Meeting.query.filter_by(status='مجدولة').count()
    }
    
    return jsonify({"stats": stats, "status": "success"})

