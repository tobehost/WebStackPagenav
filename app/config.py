import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 获取项目根目录
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # 配置密钥
    SECRET_KEY = os.getenv('SECRET_KEY', '89854663')
    
    # 使用相对路径，SQLite 会在实例文件夹中创建数据库文件
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///navsite.db'
    
    # 关闭 SQLAlchemy 的事件追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}