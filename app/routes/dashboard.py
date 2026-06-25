from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task, Tower, User, Alert, Notification
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')

@dashboard_bp.route('/')
@login_required
def index():
    open_tasks = Task.query.filter(Task.status.in_(['new', 'in_progress'])).count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    delayed_tasks = Task.query.filter_by(status='delayed').count()
    
    total_towers = Tower.query.count()
    offline_towers = Tower.query.filter_by(connection_status='offline').count()
    
    top_technicians = db.session.query(
        User.full_name,
        func.count(Task.id).label('tasks_count')
    ).join(Task, Task.technician_id == User.id).filter(
        Task.status == 'completed'
    ).group_by(User.id).order_by(func.count(Task.id).desc()).limit(5).all()
    
    top_problem_towers = db.session.query(
        Tower.name,
        func.count(Task.id).label('task_count')
    ).join(Task).group_by(Tower.id).order_by(func.count(Task.id).desc()).limit(5).all()
    
    recent_alerts = Alert.query.filter_by(is_resolved=False).order_by(Alert.created_at.desc()).limit(10).all()
    
    my_tasks = []
    if current_user.is_technician():
        my_tasks = Task.query.filter_by(technician_id=current_user.id).order_by(Task.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html',
        open_tasks=open_tasks,
        completed_tasks=completed_tasks,
        delayed_tasks=delayed_tasks,
        total_towers=total_towers,
        offline_towers=offline_towers,
        top_technicians=top_technicians,
        top_problem_towers=top_problem_towers,
        recent_alerts=recent_alerts,
        my_tasks=my_tasks
    )

@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    task_stats = db.session.query(
        Task.status,
        func.count(Task.id).label('count')
    ).group_by(Task.status).all()
    
    tower_stats = db.session.query(
        Tower.connection_status,
        func.count(Tower.id).label('count')
    ).group_by(Tower.connection_status).all()
    
    priority_stats = db.session.query(
        Task.priority,
        func.count(Task.id).label('count')
    ).group_by(Task.priority).all()
    
    return jsonify({
        'task_status': {stat[0]: stat[1] for stat in task_stats},
        'tower_status': {stat[0]: stat[1] for stat in tower_stats},
        'priority': {stat[0]: stat[1] for stat in priority_stats}
    })
