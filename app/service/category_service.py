# app/service/category_service.py
from app.models.category import Category
from app.extensions.sqlite_db import db

class CategoryService:
    @staticmethod
    def get_all_categories():
        """获取所有分类"""
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        """通过ID获取分类"""
        return Category.query.get(category_id)

    @staticmethod
    def create_category(name, icon=None, description=None, sort_order=0, is_active=True):
        """创建新分类"""
        new_category = Category(
            name=name,
            icon=icon,
            description=description,
            sort_order=sort_order,
            is_active=is_active
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def update_category(category_id, name=None, icon=None, description=None, sort_order=None, is_active=None):
        """更新分类信息"""
        category = Category.query.get(category_id)
        if category:
            if name is not None:
                category.name = name
            if icon is not None:
                category.icon = icon
            if description is not None:
                category.description = description
            if sort_order is not None:
                category.sort_order = sort_order
            if is_active is not None:
                category.is_active = is_active
            db.session.commit()
        return category
    
    @staticmethod
    def delete_category(category_id):
        """删除分类"""
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
