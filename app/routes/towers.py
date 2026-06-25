from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Tower, Alert

towers_bp = Blueprint('towers', __name__, url_prefix='/towers')

@towers_bp.route('/')
@login_required
def list_towers():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Tower.query
    if status:
        query = query.filter_by(connection_status=status)
    
    towers = query.paginate(page=page, per_page=20)
    return render_template('towers/list.html', towers=towers)

@towers_bp.route('/<int:tower_id>')
@login_required
def view_tower(tower_id):
    tower = Tower.query.get_or_404(tower_id)
    tasks = tower.tasks
    alerts = Alert.query.filter_by(tower_id=tower_id).order_by(Alert.created_at.desc()).limit(20).all()
    return render_template('towers/view.html', tower=tower, tasks=tasks, alerts=alerts)

@towers_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_tower():
    if not current_user.can_manage_towers():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        tower = Tower(
            name=request.form.get('name'),
            location=request.form.get('location'),
            latitude=float(request.form.get('latitude', 0)),
            longitude=float(request.form.get('longitude', 0)),
            ip_address=request.form.get('ip_address'),
            tower_type=request.form.get('tower_type'),
            notes=request.form.get('notes')
        )
        db.session.add(tower)
        db.session.commit()
        flash('تم إنشاء البرج بنجاح', 'success')
        return redirect(url_for('towers.view_tower', tower_id=tower.id))
    
    return render_template('towers/create.html')
