import os
from app import create_app, db
from app.models import Role, User, Tower, Setting
from datetime import datetime

def init_database():
    """Initialize database with seed data"""
    app = create_app('development')
    
    with app.app_context():
        db.create_all()
        
        # Create roles
        roles = [
            Role(
                name='admin',
                name_ar='مدير النظام',
                description='المدير الرئيسي للنظام',
                permissions={
                    'manage_users': True,
                    'manage_tasks': True,
                    'manage_towers': True,
                    'manage_settings': True,
                    'view_reports': True,
                    'export_reports': True,
                }
            ),
            Role(
                name='supervisor',
                name_ar='المشرف',
                description='مشرف المشاريع والمهام',
                permissions={
                    'manage_tasks': True,
                    'view_reports': True,
                    'export_reports': True,
                }
            ),
            Role(
                name='technician',
                name_ar='الفني',
                description='فني الصيانة والتركيب',
                permissions={
                    'view_reports': True,
                }
            ),
        ]
        
        for role in roles:
            if not Role.query.filter_by(name=role.name).first():
                db.session.add(role)
        
        db.session.commit()
        
        # Create admin user
        admin_role = Role.query.filter_by(name='admin').first()
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@alcasbah.net',
                full_name='مدير النظام',
                phone='966500000000',
                role_id=admin_role.id,
                is_active=True,
                is_verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create supervisor user
        supervisor_role = Role.query.filter_by(name='supervisor').first()
        if not User.query.filter_by(username='supervisor').first():
            supervisor = User(
                username='supervisor',
                email='supervisor@alcasbah.net',
                full_name='محمد علي - المشرف',
                phone='966500000001',
                role_id=supervisor_role.id,
                is_active=True,
                is_verified=True
            )
            supervisor.set_password('supervisor123')
            db.session.add(supervisor)
        
        # Create technician users
        technician_role = Role.query.filter_by(name='technician').first()
        technicians = [
            {'username': 'tech1', 'name': 'أحمد محمد - فني كهرباء', 'phone': '966500000002'},
            {'username': 'tech2', 'name': 'محمود أحمد - فني شبكات', 'phone': '966500000003'},
            {'username': 'tech3', 'name': 'علي سارة - فني صيانة', 'phone': '966500000004'},
        ]
        
        for tech in technicians:
            if not User.query.filter_by(username=tech['username']).first():
                user = User(
                    username=tech['username'],
                    email=f"{tech['username']}@alcasbah.net",
                    full_name=tech['name'],
                    phone=tech['phone'],
                    role_id=technician_role.id,
                    is_active=True,
                    is_verified=True
                )
                user.set_password('tech123')
                db.session.add(user)
        
        db.session.commit()
        
        # Create towers
        towers_data = [
            {
                'name': 'برج الرياض 1',
                'location': 'شارع الملك فهد - الرياض',
                'latitude': 24.7136,
                'longitude': 46.6753,
                'ip_address': '192.168.1.1',
                'tower_type': 'BTS',
                'subscribers_count': 1500,
                'notes': 'برج رئيسي'
            },
            {
                'name': 'برج الرياض 2',
                'location': 'شارع العروبة - الرياض',
                'latitude': 24.7210,
                'longitude': 46.6787,
                'ip_address': '192.168.1.2',
                'tower_type': 'Macro',
                'subscribers_count': 2000,
                'notes': 'برج فرعي'
            },
        ]
        
        for tower_data in towers_data:
            if not Tower.query.filter_by(name=tower_data['name']).first():
                tower = Tower(**tower_data, connection_status='online')
                db.session.add(tower)
        
        db.session.commit()
        
        print('✅ تم تهيئة قاعدة البيانات بنجاح!')
        print('📂 البيانات التجريبية المضافة:')
        print('   - 3 صلاحيات')
        print('   - 5 مستخدمين')
        print('   - 2 أبراج')
        print('\n👥 بيانات تسجيل الدخول:')
        print('   Admin: admin / admin123')
        print('   Supervisor: supervisor / supervisor123')
        print('   Technician: tech1, tech2, tech3 / tech123')

if __name__ == '__main__':
    init_database()
