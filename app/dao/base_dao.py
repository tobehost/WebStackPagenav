# app/dao/base_dao.py
from sqlalchemy.orm import Session
from app.extensions.sqlite_db import db

class BaseDAO:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        return db.session.query(self.model).get(id)

    def get_all(self):
        return db.session.query(self.model).all()

    def add(self, instance):
        db.session.add(instance)
        db.session.commit()

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
        return instance

    