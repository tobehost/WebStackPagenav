"""扩展初始化模块
此模块用于集中管理所有 Flask 扩展的实例化和初始化。
"""
from flask_login import LoginManager
from .sqlite_db import db, init_db

# 创建登录管理器实例
login_manager = LoginManager()

def init_extensions(app):
    """初始化所有扩展
    
    Args:
        app: Flask 应用实例
    """
    # 初始化数据库
    init_db(app)
    
    # 初始化登录管理器
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'