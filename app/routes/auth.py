from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions.sqlite_db import db
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.index'))
        else:
            flash('用户名或密码错误，或没有管理员权限')

    return render_template('admin/login.html')

@bp.route('/reset_password', methods=['POST'])
def reset_password():
    """处理密码重置请求"""
    username = request.form.get('username')
    own_reset = request.form.get('own_reset')
    new_password = request.form.get('new_password')
    
    if not all([username, own_reset, new_password]):
        flash('请填写所有必要信息', 'error')
        return redirect(url_for('auth.login'))
    
    # 验证找回密码凭证格式
    if not own_reset.isdigit() or len(own_reset) != 6:
        flash('找回密码凭证必须是6位数字', 'error')
        return redirect(url_for('auth.login'))
    
    # 查找用户并验证凭证
    user = User.query.filter_by(username=username).first()
    if not user or user.own_reset != own_reset:
        flash('用户名或找回密码凭证错误', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # 更新密码
        user.set_password(new_password)
        db.session.commit()
        flash('密码重置成功，请使用新密码登录', 'success')
    except Exception as e:
        db.session.rollback()
        flash('密码重置失败，请重试', 'error')
    
    return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出登录')
    return redirect(url_for('main.index'))