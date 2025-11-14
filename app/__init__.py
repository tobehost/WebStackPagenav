# app/__init__.py
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from app.admin import init_admin
from app.extensions.sqlite_db import init_db, db
from flask_login import LoginManager
from app.config import config

# 初始化扩展
# db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    # 使用统一的模板目录
    app = Flask(__name__,
                template_folder='../templates',  # 指向根目录的templates
                static_folder='../static')       # 指向根目录的static
    
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    init_db(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # 注册蓝图
    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # 初始化数据库和管理员
    init_database(app)
    
    # 初始化Flask-Admin
    init_admin(app)
    
    return app

def init_database(app):
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                # email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("已创建默认管理员账户: admin / admin123")

def init_admin(app):
    """初始化Flask-Admin"""
    from flask_admin import Admin
    from app.admin.views import DashboardView, CategoryView, LinkView, UserView
    from app.models import Category, Link, User
    
    # 创建管理后台实例
    admin = Admin(
        app, 
        name='导航站管理后台', 
        template_mode='bootstrap3',
        index_view=DashboardView(name='仪表盘', url='/admin', endpoint='admin')
    )
    
    # 添加管理视图
    admin.add_view(CategoryView(Category, db.session, name='分类管理', endpoint='category'))
    admin.add_view(LinkView(Link, db.session, name='链接管理', endpoint='link'))
    admin.add_view(UserView(User, db.session, name='用户管理', endpoint='user'))