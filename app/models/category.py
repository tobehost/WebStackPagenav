# app/models/category.py
from app.extensions.sqlite_db import db
from datetime import datetime
from .link import Link


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
