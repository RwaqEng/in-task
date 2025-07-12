
from flask import Blueprint, jsonify, request
from models import Task, Meeting, MeetingOutput
from extensions import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@api_bp.route('/api/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([meeting.to_dict() for meeting in meetings])

@api_bp.route('/api/meeting_outputs', methods=['GET'])
def get_meeting_outputs():
    outputs = MeetingOutput.query.all()
    return jsonify([output.to_dict() for output in outputs])
