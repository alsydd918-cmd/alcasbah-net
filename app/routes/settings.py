from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Setting, Role

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/')
@login_required
def index():
    if not current_user.is_admin():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    settings = Setting.query.all()
    return render_template('settings/index.html', settings=settings)

@settings_bp.route('/general', methods=['GET', 'POST'])
@login_required
def general():
    if not current_user.is_admin():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        for key, value in request.form.items():
            setting = Setting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = Setting(key=key, value=value)
            db.session.add(setting)
        
        db.session.commit()
        flash('تم حفظ الإعدادات بنجاح', 'success')
        return redirect(url_for('settings.general'))
    
    settings = {s.key: s.value for s in Setting.query.all()}
    return render_template('settings/general.html', settings=settings)

@settings_bp.route('/roles', methods=['GET', 'POST'])
@login_required
def roles():
    if not current_user.is_admin():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        role_id = request.form.get('role_id')
        role = Role.query.get_or_404(role_id)
        
        permissions = {
            'manage_users': 'manage_users' in request.form,
            'manage_tasks': 'manage_tasks' in request.form,
            'manage_towers': 'manage_towers' in request.form,
            'manage_settings': 'manage_settings' in request.form,
            'view_reports': 'view_reports' in request.form,
            'export_reports': 'export_reports' in request.form,
        }
        
        role.permissions = permissions
        db.session.commit()
        
        flash('تم تحديث الصلاحيات', 'success')
        return redirect(url_for('settings.roles'))
    
    roles = Role.query.all()
    return render_template('settings/roles.html', roles=roles)
