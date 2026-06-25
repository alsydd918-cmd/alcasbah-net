from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Role

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
@login_required
def list_users():
    if not current_user.can_manage_users():
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('users/list.html', users=users)

@users_bp.route('/<int:user_id>')
@login_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/view.html', user=user)

@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if not current_user.can_manage_users() and current_user.id != user_id:
        flash('ليس لديك صلاحية', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        
        if current_user.can_manage_users():
            user.role_id = request.form.get('role_id')
            user.is_active = request.form.get('is_active') == 'on'
        
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        
        db.session.commit()
        flash('تم تحديث البيانات بنجاح', 'success')
        return redirect(url_for('users.view_user', user_id=user.id))
    
    roles = Role.query.all()
    return render_template('users/edit.html', user=user, roles=roles)
