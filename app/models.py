from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import validates
from .extensions.sqlite_db import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    own_reset = db.Column(db.String(6), info={'label': '找回密码凭证', 'description': '预设密码是找回密码的凭证，限定为6位数字'})
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @validates('own_reset')
    def validate_own_reset(self, key, value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError('找回密码凭证必须是6位数字')
        return value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 使用双向关系明确声明，确保 Link 模型上存在可访问的 `category` 属性
    links = db.relationship('Link', back_populates='category', lazy=True)

    @property
    def link_count(self):
        """返回该分类下的链接数量（动态查询，以保证最新数据）。"""
        try:
            return Link.query.filter_by(category_id=self.id).count()
        except Exception:
            # 如果在没有应用上下文时访问，退回到已加载的 relationship 长度
            return len(self.links) if self.links is not None else 0

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    logo = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_hot = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # 明确定义反向关系，便于在管理界面或表单中引用 Link.category
    category = db.relationship('Category', back_populates='links')