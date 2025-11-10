# 视图包初始化文件
from .admin_model_view import AdminModelView
from .category_view import CategoryView
from .link_view import LinkView
from .user_view import UserView

__all__ = ['AdminModelView', 'CategoryView', 'LinkView', 'UserView']

def init_admin(admin, db_session):
    """初始化 Admin 视图"""
    # 注册具体模型的视图
    from app.models import User, Category, Link

    try:
        admin.add_view(UserView(User, db_session, name='用户管理', endpoint='user'))
    except Exception as e:
        print(f'Failed to add UserView: {e}')

    try:
        admin.add_view(CategoryView(Category, db_session, name='分类管理', endpoint='category'))
    except Exception as e:
        print(f'Failed to add CategoryView: {e}')

    try:
        admin.add_view(LinkView(Link, db_session, name='链接管理', endpoint='link'))
    except Exception as e:
        print(f'Failed to add LinkView: {e}')

    return admin