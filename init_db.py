from werkzeug.security import generate_password_hash
from datetime import datetime, date
import json

def init_database(app, db):
    """Initialize the database with sample data using SQLAlchemy"""
    
    with app.app_context():
        # Import models
        from models import User, Task, Meeting, MeetingOutput
        
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if User.query.first():
            print("Database already initialized!")
            return
        
        # Insert sample users
        users_data = [
            {
                'name': 'ماجد',
                'email': 'majed@rwaqeng.com',
                'password': generate_password_hash('Maj@100200300'),
                'position': 'الرئيس التنفيذي',
                'department': 'الإدارة العليا',
                'join_date': date(2020, 1, 15),
                'manager_id': None,
                'permissions': ['manage_users', 'create_tasks', 'edit_tasks', 'delete_tasks', 'view_tasks', 'manage_meetings', 'create_reports', 'view_reports', 'manage_permissions', 'view_analytics']
            },
            {
                'name': 'أصالة السعف',
                'email': 'asala.alsaaf@rwaqeng.com',
                'password': generate_password_hash('100200300@Aasala'),
                'position': 'مدير تطوير الأعمال',
                'department': 'تطوير الأعمال',
                'join_date': date(2021, 2, 2),
                'manager_id': 1,
                'permissions': ['create_tasks', 'edit_tasks', 'view_tasks', 'manage_meetings', 'create_reports', 'view_reports']
            },
            {
                'name': 'مهند',
                'email': 'muhanad.bk@rwaqeng.com',
                'password': generate_password_hash('Muh@100200300'),
                'position': 'نائب الرئيس',
                'department': 'الإدارة العليا',
                'join_date': date(2020, 3, 10),
                'manager_id': 1,
                'permissions': ['manage_users', 'create_tasks', 'edit_tasks', 'view_tasks', 'manage_meetings', 'view_reports']
            },
            {
                'name': 'نوار السماني',
                'email': 'nawar.sammani@rwaqeng.com',
                'password': generate_password_hash('Naw@100200300'),
                'position': 'مدير القسم الفني',
                'department': 'القسم الفني',
                'join_date': date(2020, 6, 1),
                'manager_id': 1,
                'permissions': ['create_tasks', 'edit_tasks', 'view_tasks', 'manage_meetings']
            },
            {
                'name': 'عبدالله ناصر',
                'email': 'abdullah.nasser@rwaqeng.com',
                'password': generate_password_hash('ABD@100200300'),
                'position': 'مدير المساحة',
                'department': 'قسم المساحة',
                'join_date': date(2021, 1, 15),
                'manager_id': 4,
                'permissions': ['create_tasks', 'edit_tasks', 'view_tasks']
            },
            {
                'name': 'عبدالله فايز',
                'email': 'abdullah.faiz@rwaqeng.com',
                'password': generate_password_hash('Abd@100200300'),
                'position': 'مهندس مساحة',
                'department': 'قسم المساحة',
                'join_date': date(2021, 8, 1),
                'manager_id': 5,
                'permissions': ['view_tasks', 'edit_tasks']
            },
            {
                'name': 'أحمد رضوان',
                'email': 'ahmed.radwan@rwaqeng.com',
                'password': generate_password_hash('Ahm@100200300'),
                'position': 'مهندس فني',
                'department': 'القسم الفني',
                'join_date': date(2022, 1, 10),
                'manager_id': 4,
                'permissions': ['view_tasks', 'edit_tasks']
            },
            {
                'name': 'إدارة الموارد البشرية',
                'email': 'hr@rwaqeng.com',
                'password': generate_password_hash('HR@100200300'),
                'position': 'مدير الموارد البشرية',
                'department': 'الموارد البشرية',
                'join_date': date(2020, 5, 1),
                'manager_id': 1,
                'permissions': ['manage_users', 'view_reports']
            },
            {
                'name': 'إبراهيم بكر',
                'email': 'ibrahim.bakr@rwaqeng.com',
                'password': generate_password_hash('Ibr@100200300'),
                'position': 'مهندس فني',
                'department': 'القسم الفني',
                'join_date': date(2022, 3, 15),
                'manager_id': 4,
                'permissions': ['view_tasks', 'edit_tasks']
            },
            {
                'name': 'جعفر الحسن',
                'email': 'jaafar.hassan@rwaqeng.com',
                'password': generate_password_hash('Jaa@100200300'),
                'position': 'مهندس مساحة',
                'department': 'قسم المساحة',
                'join_date': date(2022, 6, 1),
                'manager_id': 5,
                'permissions': ['view_tasks', 'edit_tasks']
            }
        ]
        
        for user_data in users_data:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                position=user_data['position'],
                department=user_data['department'],
                join_date=user_data['join_date'],
                manager_id=user_data['manager_id']
            )
            user.set_permissions(user_data['permissions'])
            db.session.add(user)
        
        # Commit users first to get their IDs
        db.session.commit()
        
        # Insert sample tasks
        tasks_data = [
            {
                'title': 'تصميم مخططات المشروع السكني',
                'description': 'تصميم وإعداد المخططات الهندسية للمشروع السكني الجديد',
                'assigned_to': 4,
                'created_by': 1,
                'priority': 'عالية',
                'status': 'قيد التنفيذ',
                'progress': 75,
                'due_date': date(2024, 12, 30)
            },
            {
                'title': 'مراجعة تقرير المساحة',
                'description': 'مراجعة وتدقيق تقرير المساحة للمشروع التجاري',
                'assigned_to': 5,
                'created_by': 1,
                'priority': 'متوسطة',
                'status': 'جديدة',
                'progress': 0,
                'due_date': date(2024, 12, 28)
            },
            {
                'title': 'إعداد عرض تقديمي للعميل',
                'description': 'تحضير عرض تقديمي شامل لعرضه على العميل',
                'assigned_to': 2,
                'created_by': 1,
                'priority': 'عالية',
                'status': 'مكتملة',
                'progress': 100,
                'due_date': date(2024, 12, 25)
            },
            {
                'title': 'فحص الموقع الهندسي',
                'description': 'إجراء فحص ميداني شامل للموقع المحدد',
                'assigned_to': 7,
                'created_by': 4,
                'priority': 'متوسطة',
                'status': 'قيد التنفيذ',
                'progress': 50,
                'due_date': date(2024, 12, 27)
            },
            {
                'title': 'تحديث قاعدة بيانات العملاء',
                'description': 'تحديث وتنظيم قاعدة بيانات العملاء الحالية',
                'assigned_to': 8,
                'created_by': 3,
                'priority': 'منخفضة',
                'status': 'جديدة',
                'progress': 0,
                'due_date': date(2025, 1, 5)
            }
        ]
        
        for task_data in tasks_data:
            task = Task(**task_data)
            db.session.add(task)
        
        # Insert sample meetings
        meetings_data = [
            {
                'title': 'اجتماع فريق التطوير',
                'description': 'مراجعة تقدم المشاريع الحالية ومناقشة الخطط المستقبلية',
                'meeting_date': datetime(2024, 12, 25, 10, 0),
                'location': 'قاعة الاجتماعات الرئيسية',
                'organizer_id': 1,
                'goal': 'مراجعة تقدم المشاريع وتحديد الأولويات',
                'reality': 'تأخير في بعض المشاريع وحاجة لموارد إضافية',
                'options': 'زيادة فريق العمل أو إعادة توزيع المهام',
                'way_forward': 'تعيين مهندس إضافي وإعادة جدولة المهام',
                'attendees': [1, 2, 3, 4]
            },
            {
                'title': 'مراجعة المشروع مع العميل',
                'description': 'عرض التقدم الحالي للمشروع ومناقشة التعديلات المطلوبة',
                'meeting_date': datetime(2024, 12, 25, 14, 0),
                'location': 'مكتب العميل',
                'organizer_id': 2,
                'goal': 'الحصول على موافقة العميل على التصاميم الحالية',
                'reality': 'العميل راضي عن التقدم لكن يريد تعديلات طفيفة',
                'options': 'تنفيذ التعديلات أو إعادة التصميم',
                'way_forward': 'تنفيذ التعديلات المطلوبة خلال أسبوع',
                'attendees': [2, 4, 5]
            },
            {
                'title': 'اجتماع الإدارة العامة',
                'description': 'مناقشة الاستراتيجية العامة للشركة والخطط المستقبلية',
                'meeting_date': datetime(2024, 12, 26, 11, 0),
                'location': 'قاعة الإدارة',
                'organizer_id': 1,
                'goal': 'وضع استراتيجية الشركة للعام القادم',
                'reality': 'نمو جيد في الأعمال وحاجة لتوسيع الفريق',
                'options': 'توظيف مهندسين جدد أو الاستعانة بمقاولين',
                'way_forward': 'البدء في عملية التوظيف الشهر القادم',
                'attendees': [1, 3, 8]
            }
        ]
        
        for meeting_data in meetings_data:
            attendees = meeting_data.pop('attendees')
            meeting = Meeting(**meeting_data)
            meeting.set_attendees(attendees)
            db.session.add(meeting)
        
        db.session.commit()
        print("Database initialized successfully with SQLAlchemy!")

if __name__ == '__main__':
    from app import create_app
    from extensions import db
    
    app = create_app()
    init_database(app, db)

