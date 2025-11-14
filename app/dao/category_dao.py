# app/dao/category_dao.py
from app.models.category import Category
from app.dao.base_dao import BaseDAO
from app.extensions.sqlite_db import db

class CategoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(Category)

    def get_by_name(self, name):
        return db.session.query(self.model).filter_by(name=name).first()
    
    def get_by_parent_id(self, parent_id):
        return db.session.query(self.model).filter_by(parent_id=parent_id).all()
    
    def delete_by_id(self, id):
        instance = self.get_by_id(id)
        if instance:
            return self.delete(instance)
        return None
    
    def update_name(self, id, new_name):
        instance = self.get_by_id(id)
        if instance:
            instance.name = new_name
            db.session.commit()
            return instance
        return None

    def update_parent_id(self, id, new_parent_id):
        instance = self.get_by_id(id)
        if instance:
            instance.parent_id = new_parent_id
            db.session.commit()
            return instance
        return None

    def get_subcategories(self, category_id):
        return db.session.query(self.model).filter_by(parent_id=category_id).all()