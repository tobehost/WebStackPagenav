# app/dao/link_dao.py
from app.models.link import Link
from app.extensions.sqlite_db import db
from sqlalchemy.orm import joinedload

class LinkDAO:
    @staticmethod
    def get_all_links():
        """获取所有链接"""
        return Link.query.options(joinedload(Link.category)).all()

    @staticmethod
    def get_link_by_id(link_id):
        """通过ID获取链接"""
        return Link.query.get(link_id)

    @staticmethod
    def create_link(name, url, category_id, description=None):
        """创建新链接"""
        new_link = Link(
            name=name,
            url=url,
            category_id=category_id,
            description=description
        )
        db.session.add(new_link)
        db.session.commit()
        return new_link

    @staticmethod
    def update_link(link_id, name=None, url=None, category_id=None, description=None):
        """更新链接信息"""
        link = Link.query.get(link_id)
        if link:
            if name is not None:
                link.name = name
            if url is not None:
                link.url = url
            if category_id is not None:
                link.category_id = category_id
            if description is not None:
                link.description = description
            db.session.commit()
        return link

    @staticmethod
    def delete_link(link_id):
        """删除链接"""
        link = Link.query.get(link_id)
        if link:
            db.session.delete(link)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_links_by_category(category_id):
        """通过分类ID获取链接"""
        return Link.query.filter_by(category_id=category_id).all()

    @staticmethod
    def search_links_by_name(name):
        """通过名称搜索链接"""
        return Link.query.filter(Link.name.ilike(f"%{name}%")).all()

    @staticmethod
    def count_links():
        """统计链接数量"""
        return Link.query.count()