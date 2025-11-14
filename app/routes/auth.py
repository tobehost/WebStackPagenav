# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user
from app.models import User

# 创建认证路由蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth')
def index():
    """
    认证模块首页
    提供认证相关的信息和链接
    """
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    
    # 可以在这里显示认证相关的信息
    return render_template('admin/login.html', show_welcome=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    # 如果用户已登录，直接跳转到管理后台
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        # 验证用户和密码
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            
            # 获取下一步要跳转的页面
            next_page = request.args.get('next')
            
            # 安全地重定向到目标页面
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            else:
                return redirect(url_for('admin.index'))
        else:
            flash('用户名或密码错误，或没有管理员权限', 'error')
            
    # 使用新的模板路径
    return render_template('admin/login.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """重置密码页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        own_reset = request.form.get('own_reset')
        new_password = request.form.get('new_password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.own_reset == own_reset:
            user.set_password(new_password)
            flash('密码重置成功，请使用新密码登录', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('用户名或找回密码凭证错误', 'error')
    
    return render_template('auth/reset_password.html')