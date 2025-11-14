# app/models/link.py
from app.extensions.sqlite_db import db
from datetime import datetime
from .category import Category


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