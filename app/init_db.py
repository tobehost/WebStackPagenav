import os
import logging
from app import create_app
from app.extensions.sqlite_db import db
from app.models import User, Category, Link

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    try:
        logger.info("正在创建应用实例...")
        app = create_app()
        
        with app.app_context():
            logger.info("正在创建数据库表...")
            db.create_all()
            
            # 创建超级管理员账户
            logger.info("检查管理员账户...")
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    own_reset='898546',
                    is_admin=True
                )
                admin.set_password('admin')
                db.session.add(admin)
                db.session.commit()
                logger.info("超级管理员账户创建成功！")
            
            # 添加示例数据
            logger.info("检查分类数据...")
            if not Category.query.first():
                # 添加分类
                categories_data = [
                    {'name': '常用推荐', 'icon': 'linecons-star'},
                    {'name': '社区资讯', 'icon': 'linecons-doc'},
                    {'name': '发现产品', 'icon': 'linecons-lightbulb'},
                    {'name': '界面灵感', 'icon': 'linecons-lightbulb'},
                    {'name': '网页灵感', 'icon': 'linecons-lightbulb'},
                    {'name': '图标素材', 'icon': 'linecons-thumbs-up'},
                    {'name': 'LOGO设计', 'icon': 'linecons-thumbs-up'},
                    {'name': '平面素材', 'icon': 'linecons-thumbs-up'},
                    {'name': 'UI资源', 'icon': 'linecons-thumbs-up'},
                    {'name': 'Sketch资源', 'icon': 'linecons-thumbs-up'},
                    {'name': '字体资源', 'icon': 'linecons-thumbs-up'},
                    {'name': 'Mockup', 'icon': 'linecons-thumbs-up'},
                    {'name': '摄影图库', 'icon': 'linecons-thumbs-up'},
                    {'name': 'PPT资源', 'icon': 'linecons-thumbs-up'},
                    {'name': '图形创意', 'icon': 'linecons-diamond'},
                    {'name': '界面设计', 'icon': 'linecons-diamond'},
                    {'name': '交互动效', 'icon': 'linecons-diamond'},
                    {'name': '在线配色', 'icon': 'linecons-diamond'},
                    {'name': '在线工具', 'icon': 'linecons-diamond'},
                    {'name': 'Chrome插件', 'icon': 'linecons-diamond'},
                    {'name': '设计规范', 'icon': 'linecons-pencil'},
                    {'name': '视频教程', 'icon': 'linecons-pencil'},
                    {'name': '设计文章', 'icon': 'linecons-pencil'},
                    {'name': '设计电台', 'icon': 'linecons-pencil'},
                    {'name': '交互设计', 'icon': 'linecons-pencil'},
                    {'name': 'UED团队', 'icon': 'linecons-user'},
                ]
                
                for cat_data in categories_data:
                    category = Category(**cat_data)
                    db.session.add(category)
                
                db.session.commit()
                logger.info("分类数据添加成功！")
                
                # 添加示例链接
                sample_links = [
                    {
                        'title': 'Dribbble',
                        'url': 'https://dribbble.com/',
                        'description': '全球UI设计师作品分享平台。',
                        'logo': 'images/logos/dribbble.png',
                        'category_id': 1
                    },
                    {
                        'title': 'Behance',
                        'url': 'https://behance.net/',
                        'description': 'Adobe旗下的设计师交流平台',
                        'logo': 'images/logos/behance.png',
                        'category_id': 1
                    }
                ]
                
                for link_data in sample_links:
                    link = Link(**link_data)
                    db.session.add(link)
                
                db.session.commit()
                logger.info("示例链接添加成功！")
            
            logger.info("数据库初始化完成！")
            
        return app
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise
        

if __name__ == '__main__':
    init_database()
    
    # 创建超级管理员账户
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            own_reset='898546',
            is_admin=True
        )
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        print("超级管理员账户创建成功！")
    
    # 添加示例数据
    if not Category.query.first():
        # 添加分类
        categories_data = [
            {'name': '常用推荐', 'icon': 'linecons-star'},
            {'name': '社区资讯', 'icon': 'linecons-doc'},
            {'name': '发现产品', 'icon': 'linecons-lightbulb'},
            {'name': '界面灵感', 'icon': 'linecons-lightbulb'},
            {'name': '网页灵感', 'icon': 'linecons-lightbulb'},
            {'name': '图标素材', 'icon': 'linecons-thumbs-up'},
            {'name': 'LOGO设计', 'icon': 'linecons-thumbs-up'},
            {'name': '平面素材', 'icon': 'linecons-thumbs-up'},
            {'name': 'UI资源', 'icon': 'linecons-thumbs-up'},
            {'name': 'Sketch资源', 'icon': 'linecons-thumbs-up'},
            {'name': '字体资源', 'icon': 'linecons-thumbs-up'},
            {'name': 'Mockup', 'icon': 'linecons-thumbs-up'},
            {'name': '摄影图库', 'icon': 'linecons-thumbs-up'},
            {'name': 'PPT资源', 'icon': 'linecons-thumbs-up'},
            {'name': '图形创意', 'icon': 'linecons-diamond'},
            {'name': '界面设计', 'icon': 'linecons-diamond'},
            {'name': '交互动效', 'icon': 'linecons-diamond'},
            {'name': '在线配色', 'icon': 'linecons-diamond'},
            {'name': '在线工具', 'icon': 'linecons-diamond'},
            {'name': 'Chrome插件', 'icon': 'linecons-diamond'},
            {'name': '设计规范', 'icon': 'linecons-pencil'},
            {'name': '视频教程', 'icon': 'linecons-pencil'},
            {'name': '设计文章', 'icon': 'linecons-pencil'},
            {'name': '设计电台', 'icon': 'linecons-pencil'},
            {'name': '交互设计', 'icon': 'linecons-pencil'},
            {'name': 'UED团队', 'icon': 'linecons-user'},
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        
        # 添加示例链接
        sample_links = [
            {
                'title': 'Dribbble',
                'url': 'https://dribbble.com/',
                'description': '全球UI设计师作品分享平台。',
                'logo': 'images/logos/dribbble.png',
                'category_id': 1
            },
            {
                'title': 'Behance',
                'url': 'https://behance.net/',
                'description': 'Adobe旗下的设计师交流平台',
                'logo': 'images/logos/behance.png',
                'category_id': 1
            }
        ]
        
        for link_data in sample_links:
            link = Link(**link_data)
            db.session.add(link)
        
        db.session.commit()
        print("数据库初始化完成！")