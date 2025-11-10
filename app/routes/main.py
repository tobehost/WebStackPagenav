from flask import Blueprint, render_template
from flask import redirect, url_for, flash, request
from flask_login import login_user, logout_user
from app.models import Category, Link, User
# from app.extensions import db,将数据迁移到cloudflare d1时使用插件
from app.models import db


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    
    # 组织数据：每个分类包含其链接
    categories_with_links = []
    for category in categories:
        links = Link.query.filter_by(
            category_id=category.id, 
            is_active=True
        ).order_by(Link.sort_order).all()
        
        categories_with_links.append({
            'category': category,
            'links': links
        })
    
    return render_template('index.html', categories_with_links=categories_with_links)

# NOTE: 登录路由移交给 auth 蓝图（app/routes/auth.py），
# 避免与 auth 蓝图的 /login 路径冲突而造成重定向循环。

@bp.route('/login_out')
def login_out():
    logout_user()
    return redirect(url_for('main.index'))