from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task, Tower, User, TaskImage, TaskComment
from datetime import datetime
import os
from werkzeug.utils import secure_filename

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
@login_required
def list_tasks():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Task.query
    
    if status:
        query = query.filter_by(status=status)
    
    if current_user.is_technician():
        query = query.filter_by(technician_id=current_user.id)
    
    tasks = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if not current_user.can_manage_tasks():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        last_task = Task.query.order_by(Task.id.desc()).first()
        task_number = f'TSK-{(last_task.id + 1 if last_task else 1):05d}'
        
        task = Task(
            task_number=task_number,
            title=request.form.get('title'),
            description=request.form.get('description'),
            tower_id=request.form.get('tower_id'),
            task_type=request.form.get('task_type'),
            priority=request.form.get('priority', 'normal'),
            status='new',
            creator_id=current_user.id
        )
        
        if request.form.get('technician_id'):
            task.technician_id = request.form.get('technician_id')
        
        db.session.add(task)
        db.session.commit()
        
        flash('تم إنشاء المهمة بنجاح', 'success')
        return redirect(url_for('tasks.view_task', task_id=task.id))
    
    towers = Tower.query.all()
    technicians = User.query.filter_by(role_id=3).all()
    
    return render_template('tasks/create.html', towers=towers, technicians=technicians)

@tasks_bp.route('/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if current_user.is_technician() and task.technician_id != current_user.id:
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    return render_template('tasks/view.html', task=task)

@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if not current_user.can_manage_tasks() and current_user.id != task.technician_id:
        return jsonify({'error': 'ليس لديك صلاحية'}), 403
    
    old_status = task.status
    task.status = request.form.get('status')
    
    if request.form.get('execution_report'):
        task.execution_report = request.form.get('execution_report')
    
    if task.status == 'completed':
        task.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('تم تحديث المهمة', 'success')
    return redirect(url_for('tasks.view_task', task_id=task_id))
