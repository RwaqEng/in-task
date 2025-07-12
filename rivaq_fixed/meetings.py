from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from rivaq_fixed.extensions import db
from rivaq_fixed.models import User, Meeting, MeetingOutput
from datetime import datetime

meetings_bp = Blueprint('meetings', __name__)

@meetings_bp.route('/')
@login_required
def meetings_list():
    if not current_user.has_permission('view_meetings'):
        flash('غير مصرح لك بعرض الاجتماعات', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status_filter = request.args.get('status', 'all')
    
    query = Meeting.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    meetings = query.order_by(Meeting.meeting_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('meetings.html', meetings=meetings, status_filter=status_filter)

@meetings_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_meeting():
    if not current_user.has_permission('manage_meetings'):
        flash('غير مصرح لك بإنشاء اجتماعات', 'error')
        return redirect(url_for('meetings.meetings_list'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        meeting_date = request.form.get('meeting_date')
        location = request.form.get('location')
        goal = request.form.get('goal')
        attendees = request.form.getlist('attendees')
        
        if not all([title, meeting_date]):
            flash('يرجى ملء الحقول المطلوبة', 'error')
            return render_template('add_meeting.html')
        
        new_meeting = Meeting(
            title=title,
            description=description,
            meeting_date=datetime.strptime(meeting_date, '%Y-%m-%dT%H:%M'),
            location=location,
            organizer_id=current_user.id,
            goal=goal
        )
        
        # Set attendees
        if attendees:
            new_meeting.set_attendees([int(a) for a in attendees])
        
        db.session.add(new_meeting)
        db.session.commit()
        
        flash('تم إنشاء الاجتماع بنجاح', 'success')
        return redirect(url_for('meetings.meetings_list'))
    
    users = User.query.all()
    return render_template('add_meeting.html', users=users)

@meetings_bp.route('/edit/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def edit_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    
    if not (current_user.has_permission('manage_meetings') or 
            meeting.organizer_id == current_user.id):
        flash('غير مصرح لك بتعديل هذا الاجتماع', 'error')
        return redirect(url_for('meetings.meetings_list'))
    
    if request.method == 'POST':
        meeting.title = request.form.get('title')
        meeting.description = request.form.get('description')
        meeting_date = request.form.get('meeting_date')
        meeting.meeting_date = datetime.strptime(meeting_date, '%Y-%m-%dT%H:%M')
        meeting.location = request.form.get('location')
        meeting.goal = request.form.get('goal')
        meeting.reality = request.form.get('reality')
        meeting.options = request.form.get('options')
        meeting.way_forward = request.form.get('way_forward')
        meeting.status = request.form.get('status')
        
        attendees = request.form.getlist('attendees')
        if attendees:
            meeting.set_attendees([int(a) for a in attendees])
        
        db.session.commit()
        flash('تم تحديث الاجتماع بنجاح', 'success')
        return redirect(url_for('meetings.meetings_list'))
    
    users = User.query.all()
    selected_attendees = meeting.get_attendees()
    
    return render_template('edit_meeting.html', meeting=meeting, users=users, 
                         selected_attendees=selected_attendees)

@meetings_bp.route('/delete/<int:meeting_id>', methods=['POST'])
@login_required
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    
    if not (current_user.has_permission('manage_meetings') or 
            meeting.organizer_id == current_user.id):
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بحذف هذا الاجتماع'}), 403
    
    db.session.delete(meeting)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'تم حذف الاجتماع بنجاح'})

@meetings_bp.route('/view/<int:meeting_id>')
@login_required
def view_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Check if user can view this meeting
    attendee_ids = meeting.get_attendees()
    if not (current_user.has_permission('view_meetings') or 
            meeting.organizer_id == current_user.id or 
            current_user.id in attendee_ids):
        flash('غير مصرح لك بعرض هذا الاجتماع', 'error')
        return redirect(url_for('meetings.meetings_list'))
    
    # Get attendees details
    attendees = []
    for attendee_id in attendee_ids:
        user = User.query.get(attendee_id)
        if user:
            attendees.append(user)
    
    return render_template('view_meeting.html', meeting=meeting, attendees=attendees)

