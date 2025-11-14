# app/service/user_service.py
from app.models.user import User
from app.extensions.sqlite_db import db

class UserService:
    @staticmethod
    def get_all_users():
        """获取所有用户"""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """通过ID获取用户"""
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, email, password_hash):
        """创建新用户"""
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, username=None, email=None, password_hash=None):
        """更新用户信息"""
        user = User.query.get(user_id)
        if user:
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if password_hash is not None:
                user.password_hash = password_hash
            db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False