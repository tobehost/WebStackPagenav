# app/dao/user_dao.py
from app.dao.base_dao import BaseDAO
from app.models.user import User
from app.extensions.sqlite_db import db

class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username):
        return db.session.query(self.model).filter_by(username=username).first()

    def get_by_email(self, email):
        return db.session.query(self.model).filter_by(email=email).first()

    def get_active_users(self):
        return db.session.query(self.model).filter_by(is_active=True).all()

    def update_email(self, user_id, new_email):
        user = self.get_by_id(user_id)
        if user:
            user.email = new_email
            db.session.commit()
        return user

    def deactivate_user(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            db.session.commit()
        return user

    def activate_user(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            user.is_active = True
            db.session.commit()
        return user

    def delete_by_username(self, username):
        user = self.get_by_username(username)
        if user:
            return self.delete(user)
        return None

    def reset_password(self, user_id, own_reset, new_password):
        user = self.get_by_id(user_id) 
        own_reset == user.own_reset
        if user:
            user.password = new_password
            db.session.commit()
        return user
