# app/models/user.py
from app.extensions.sqlite_db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    own_reset = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())

    @validates('own_reset')
    def validate_own_reset(self, key, value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError('找回密码凭证必须是6位数字')
        return value
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
