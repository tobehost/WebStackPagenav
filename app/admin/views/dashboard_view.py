# app/admin/views/dashboard_view.py
from flask import redirect, url_for, render_template
from flask_login import current_user, login_required
from flask_admin import BaseView, expose
from app.models import Category, Link, User
from datetime import datetime

class DashboardView(BaseView):
    """
    仪表盘视图，显示管理后台的概览信息
    """
    
    @expose('/')
    @login_required
    def index(self):
        """仪表盘首页"""
        if not current_user.is_admin:
            return redirect(url_for('main.index'))
        
        # 获取统计数据
        category_count = Category.query.count()
        link_count = Link.query.count()
        user_count = User.query.count()
        active_link_count = Link.query.filter_by(is_active=True).count()
        
        # 获取最近添加的链接
        recent_links = Link.query.order_by(Link.created_at.desc()).limit(5).all()
        
        # 获取分类统计
        category_stats = []
        categories = Category.query.all()
        for category in categories:
            link_count_in_category = Link.query.filter_by(category_id=category.id).count()
            active_link_count_in_category = Link.query.filter_by(
                category_id=category.id, is_active=True
            ).count()
            
            category_stats.append({
                'name': category.name,
                'total_links': link_count_in_category,
                'active_links': active_link_count_in_category
            })
        
        # 使用新的模板路径
        return render_template(
            'admin/index.html',  # 现在在 templates/admin/index.html
            category_count=category_count,
            link_count=link_count,
            user_count=user_count,
            active_link_count=active_link_count,
            recent_links=recent_links,
            category_stats=category_stats,
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    @expose('/stats')
    @login_required
    def stats(self):
        """统计页面"""
        if not current_user.is_admin:
            return redirect(url_for('main.index'))
        
        return self.render('admin/stats.html')  # 更新模板路径
    
    def is_accessible(self):
        """检查访问权限"""
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        """无权限访问时的回调"""
        return redirect(url_for('auth.login'))