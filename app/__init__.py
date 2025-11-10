import os
from flask import Flask
from dotenv import load_dotenv

def create_app(config_name='default', init_admin=False):
    """应用工厂函数
    
    Args:
        config_name: 配置名称，默认为 'default'
        init_admin: 是否初始化 Flask-Admin，默认为 False

    Returns:
        Flask 应用实例
    """
    # 加载环境变量（如果存在）
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    load_dotenv(os.path.join(base_dir, '.env'))

    # 创建应用实例
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),  # 使用绝对路径
        static_folder=os.path.join(base_dir, 'static')       # 使用绝对路径
    )

    # 基本配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '89854663')
    
    # 确保实例目录存在
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 初始化所有扩展
    from .extensions import init_extensions, login_manager
    from .extensions.sqlite_db import db, init_db
    
    # 初始化扩展
    init_extensions(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # 注册蓝图
    from .routes.main import bp as main_bp
    from .routes.auth import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # 可选地初始化 Flask-Admin
    if init_admin:
        try:
            from flask_admin import Admin
            admin = Admin(app, name='导航站管理后台', template_mode='bootstrap3')
            from .admin.views import init_admin as register_admin_views
            register_admin_views(admin, db.session)
        except ImportError:
            app.logger.warning('flask_admin 未安装，跳过 Admin 初始化')
        except Exception as e:
            app.logger.warning(f'初始化 Flask-Admin 视图时发生错误: {e}')

    # 初始化数据库表
    with app.app_context():
        db.create_all()

    return app