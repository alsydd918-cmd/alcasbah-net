from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import MikroTikDevice, Tower, Alert
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

mikrotik_bp = Blueprint('mikrotik', __name__, url_prefix='/mikrotik')

@mikrotik_bp.route('/devices')
@login_required
def list_devices():
    if not current_user.can_manage_towers():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    devices = MikroTikDevice.query.paginate(page=page, per_page=20)
    return render_template('mikrotik/devices.html', devices=devices)

@mikrotik_bp.route('/device/create', methods=['GET', 'POST'])
@login_required
def create_device():
    if not current_user.can_manage_towers():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        device = MikroTikDevice(
            name=request.form.get('name'),
            ip_address=request.form.get('ip_address'),
            username=request.form.get('username'),
            password=request.form.get('password'),
            location=request.form.get('location'),
            tower_id=request.form.get('tower_id')
        )
        db.session.add(device)
        db.session.commit()
        
        flash('تم إضافة الجهاز بنجاح', 'success')
        return redirect(url_for('mikrotik.list_devices'))
    
    towers = Tower.query.all()
    return render_template('mikrotik/create_device.html', towers=towers)

@mikrotik_bp.route('/device/<int:device_id>')
@login_required
def view_device(device_id):
    device = MikroTikDevice.query.get_or_404(device_id)
    alerts = Alert.query.filter_by(tower_id=device.tower_id).order_by(Alert.created_at.desc()).limit(20).all()
    return render_template('mikrotik/view_device.html', device=device, alerts=alerts)

@mikrotik_bp.route('/monitor')
@login_required
def monitor():
    if not current_user.can_manage_towers():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    devices = MikroTikDevice.query.filter_by(is_active=True).all()
    return render_template('mikrotik/monitor.html', devices=devices)
