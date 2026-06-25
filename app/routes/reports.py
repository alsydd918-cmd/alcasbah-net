from flask import Blueprint, render_template, request, send_file, jsonify
from flask_login import login_required, current_user
from app.models import Task, Tower, User
from datetime import datetime
import io

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')

@reports_bp.route('/tasks')
@login_required
def tasks_report():
    filters = {}
    
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    tower_id = request.args.get('tower_id', '')
    
    query = Task.query
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if tower_id:
        query = query.filter_by(tower_id=tower_id)
    
    tasks = query.all()
    towers = Tower.query.all()
    
    return render_template('reports/tasks.html', tasks=tasks, towers=towers, filters=filters)

@reports_bp.route('/towers')
@login_required
def towers_report():
    towers = Tower.query.all()
    return render_template('reports/towers.html', towers=towers)

@reports_bp.route('/statistics')
@login_required
def statistics():
    from app import db
    from sqlalchemy import func
    
    task_stats = db.session.query(
        Task.status,
        func.count(Task.id).label('count')
    ).group_by(Task.status).all()
    
    tower_stats = db.session.query(
        Tower.connection_status,
        func.count(Tower.id).label('count')
    ).group_by(Tower.connection_status).all()
    
    return render_template('reports/statistics.html',
        task_stats=task_stats,
        tower_stats=tower_stats
    )
