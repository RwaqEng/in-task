from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

# تصحيح مسار الاستيراد
from rivaq_fixed.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.Date)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    permissions = db.Column(db.Text)
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('User', remote_side=[id], backref='subordinates')
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by', backref='creator')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to', backref='assignee')
    organized_meetings = db.relationship('Meeting', backref='organizer')
    
    def get_permissions(self):
        """Get user permissions as a list"""
        if self.permissions:
            return json.loads(self.permissions)
        return []
    
    def set_permissions(self, permissions_list):
        """Set user permissions from a list"""
        self.permissions = json.dumps(permissions_list)
    
    def has_permission(self, permission):
        """Check if user has a specific permission"""
        return permission in self.get_permissions()

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    priority = db.Column(db.String(50), default='متوسطة')
    status = db.Column(db.String(50), default='جديدة')
    progress = db.Column(db.Integer, default=0)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    meeting_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goal = db.Column(db.Text)
    reality = db.Column(db.Text)
    options = db.Column(db.Text)
    way_forward = db.Column(db.Text)
    attendees = db.Column(db.Text)  # JSON string of attendee IDs
    status = db.Column(db.String(50), default='مجدولة')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    outputs = db.relationship('MeetingOutput', backref='meeting', cascade='all, delete-orphan')
    
    def get_attendees(self):
        """Get meeting attendees as a list of IDs"""
        if self.attendees:
            return json.loads(self.attendees)
        return []
    
    def set_attendees(self, attendee_ids):
        """Set meeting attendees from a list of IDs"""
        self.attendees = json.dumps(attendee_ids)

class MeetingOutput(db.Model):
    __tablename__ = 'meeting_outputs'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))
    output_type = db.Column(db.String(100))
    content = db.Column(db.Text)
    responsible_person = db.Column(db.Integer, db.ForeignKey('users.id'))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='جديدة')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    responsible = db.relationship('User', backref='meeting_outputs')

