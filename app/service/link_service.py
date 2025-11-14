# app/service/link_service.py
from app.models.link import Link
from app.extensions import db


class LinkService:
    @staticmethod
    def get_all_links():
        """获取所有链接"""
        return Link.query.all()

    @staticmethod
    def get_link_by_id(link_id):
        """通过ID获取链接"""
        return Link.query.get(link_id)

    @staticmethod
    def create_link(name, url):
        """创建新链接"""
        new_link = Link(name=name, url=url)
        db.session.add(new_link)
        db.session.commit()
        return new_link

    @staticmethod
    def update_link(link_id, name=None, url=None):
        """更新链接信息"""
        link = Link.query.get(link_id)
        if link:
            if name:
                link.name = name
            if url:
                link.url = url
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

# db.init_app(app)
# db.create_all()
