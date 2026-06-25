from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class Role(db.Model):
    """User roles"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    permissions = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    users = db.relationship('User', backref='role', lazy=True)
    
    def has_permission(self, permission):
        return self.permissions.get(permission, False)

class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks_assigned = db.relationship('Task', backref='technician', foreign_keys='Task.technician_id', lazy=True)
    tasks_created = db.relationship('Task', backref='creator', foreign_keys='Task.creator_id', lazy=True)
    comments = db.relationship('TaskComment', backref='author', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission):
        return self.role.has_permission(permission) if self.role else False
    
    def can_manage_users(self):
        return self.has_permission('manage_users')
    
    def can_manage_tasks(self):
        return self.has_permission('manage_tasks')
    
    def can_manage_towers(self):
        return self.has_permission('manage_towers')
    
    def is_admin(self):
        return self.role.name == 'admin' if self.role else False
    
    def is_supervisor(self):
        return self.role.name == 'supervisor' if self.role else False
    
    def is_technician(self):
        return self.role.name == 'technician' if self.role else False
    
    def __repr__(self):
        return f'<User {self.username}>'

class Tower(db.Model):
    """Tower/Cell site model"""
    __tablename__ = 'towers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    ip_address = db.Column(db.String(50), unique=True)
    tower_type = db.Column(db.String(50), default='Cell Site')
    
    connection_status = db.Column(db.String(20), default='online')
    subscribers_count = db.Column(db.Integer, default=0)
    
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks = db.relationship('Task', backref='tower', lazy=True)
    mikrotik_devices = db.relationship('MikroTikDevice', backref='tower', lazy=True)
    alerts = db.relationship('Alert', backref='tower', lazy=True)
    
    def __repr__(self):
        return f'<Tower {self.name}>'

class MikroTikDevice(db.Model):
    """MikroTik device model"""
    __tablename__ = 'mikrotik_devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    
    tower_id = db.Column(db.Integer, db.ForeignKey('towers.id'))
    
    is_active = db.Column(db.Boolean, default=True)
    last_check = db.Column(db.DateTime)
    connection_status = db.Column(db.String(20), default='unknown')
    ping_time = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MikroTikDevice {self.name}>'

class Task(db.Model):
    """Task/Work order model"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    
    tower_id = db.Column(db.Integer, db.ForeignKey('towers.id'), nullable=False, index=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    task_type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), default='normal')
    status = db.Column(db.String(20), default='new', index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    execution_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    execution_report = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    images = db.relationship('TaskImage', backref='task', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('TaskComment', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.task_number}>'

class TaskImage(db.Model):
    """Task image attachments"""
    __tablename__ = 'task_images'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False, index=True)
    
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20))
    file_size = db.Column(db.Integer)
    
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TaskImage {self.filename}>'

class TaskComment(db.Model):
    """Task comments/notes"""
    __tablename__ = 'task_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TaskComment {self.id}>'

class Notification(db.Model):
    """User notifications"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))
    
    related_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Alert(db.Model):
    """System alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    tower_id = db.Column(db.Integer, db.ForeignKey('towers.id'), index=True)
    
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50))
    
    severity = db.Column(db.String(20), default='medium')
    is_resolved = db.Column(db.Boolean, default=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)

class Log(db.Model):
    """Activity/Audit logs"""
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    action = db.Column(db.String(100), nullable=False, index=True)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Log {self.action}>'

class Setting(db.Model):
    """System settings"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Setting {self.key}>'
