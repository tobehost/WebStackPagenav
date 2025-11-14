# 视图包初始化文件
from .admin_model_view import AdminModelView
from .category_view import CategoryView
from .link_view import LinkView
from .user_view import UserView
from .dashboard_view import DashboardView

__all__ = [
    'AdminModelView', 
    'CategoryView', 
    'LinkView', 
    'UserView',
    'DashboardView'
]

def init_admin(app):
    """初始化Flask-Admin"""
    from flask_admin import Admin
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
    return admin