"""SQLite 数据库配置

此模块负责配置和初始化 SQLite 数据库连接。
配置项从 .env 文件中读取，包括:
- DATABASE_URL: 数据库文件路径 (可选，默认为 instance/navsite.db)
- DB_POOL_SIZE: 连接池大小 (可选，默认为 5)
- DB_POOL_TIMEOUT: 连接池超时时间 (可选，默认为 10)
- DB_POOL_RECYCLE: 连接池回收时间 (可选，默认为 3600)
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path
import logging

# 创建全局 SQLAlchemy 实例
db = SQLAlchemy()
migrate = Migrate()

# 配置日志
logger = logging.getLogger(__name__)

def get_db_config(app):
    """获取数据库配置
    
    Args:
        app: Flask 应用实例
    
    Returns:
        dict: 数据库配置字典
    """
    base_dir = Path(app.root_path).parent
    
    # 使用内存数据库进行测试
    db_path = os.getenv('DATABASE_URL') or 'sqlite:///navsite.db'
    
    # 连接池配置
    pool_size = int(os.getenv('DB_POOL_SIZE', '5'))
    pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '10'))
    pool_recycle = int(os.getenv('DB_POOL_RECYCLE', '3600'))
    
    return {
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_size': pool_size,
            'pool_timeout': pool_timeout,
            'pool_recycle': pool_recycle,
            'pool_pre_ping': True,  # 自动检测断开的连接
        }
    }

def init_db(app):
    """初始化数据库
    
    Args:
        app: Flask 应用实例
    """
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        db_path = os.path.join(base_dir, 'instance', 'navsite.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 获取配置
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # 初始化 SQLAlchemy
        db.init_app(app)
        
        # 初始化数据库迁移
        migrate.init_app(app, db, directory='migrations')
        
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise
