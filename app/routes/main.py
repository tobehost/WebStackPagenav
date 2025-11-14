# app/routes/main.py
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import current_user, logout_user, login_required
from app.models import Category, Link
import os

# 创建前台路由蓝图
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """网站首页"""
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

@main_bp.route('/logout')
@login_required
def logout():
    """退出登录"""
    logout_user()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/debug/routes')
def debug_routes():
    """调试路由：打印所有路由信息"""
    if not current_app.debug:
        flash('此功能仅在调试模式下可用', 'warning')
        return redirect(url_for('main.index'))
    
    output = []
    output.append("=" * 80)
    output.append("应用程序路由列表")
    output.append("=" * 80)
    
    # 收集所有路由信息
    routes = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        routes.append({
            'endpoint': rule.endpoint,
            'methods': methods,
            'path': str(rule),
            'is_admin': 'admin' in rule.endpoint or '/admin' in str(rule)
        })
    
    # 按路径排序
    routes.sort(key=lambda x: x['path'])
    
    # 格式化为输出
    output.append(f"{'路径':<40} {'方法':<20} {'端点':<30} {'类型'}")
    output.append("-" * 80)
    
    for route in routes:
        route_type = "管理后台" if route['is_admin'] else "前台"
        output.append(f"{route['path']:<40} {route['methods']:<20} {route['endpoint']:<30} {route_type}")
    
    output.append("=" * 80)
    output.append(f"总计: {len(routes)} 个路由")
    
    # 统计信息
    admin_routes = len([r for r in routes if r['is_admin']])
    frontend_routes = len(routes) - admin_routes
    output.append(f"前台路由: {frontend_routes} 个")
    output.append(f"管理路由: {admin_routes} 个")
    output.append("=" * 80)
    
    # 返回纯文本响应
    return '<pre>' + '\n'.join(output) + '</pre>'

@main_bp.route('/debug/routes/json')
def debug_routes_json():
    """调试路由：以JSON格式返回路由信息"""
    if not current_app.debug:
        return {'error': '此功能仅在调试模式下可用'}, 403
    
    routes_info = []
    for rule in current_app.url_map.iter_rules():
        # 过滤掉静态文件路由
        if rule.endpoint == 'static':
            continue
            
        # 检查是否是认证路由
        is_auth_route = rule.endpoint.startswith('auth.')
        
        route_info = {
            'endpoint': rule.endpoint,
            'methods': list(rule.methods - {'OPTIONS', 'HEAD'}),
            'path': str(rule),
            'is_admin_route': any(keyword in rule.endpoint for keyword in ['admin', 'category', 'link', 'user']),
            'is_auth_route': is_auth_route,
            'is_main_route': rule.endpoint.startswith('main.')
        }
        routes_info.append(route_info)
    
    # 添加统计信息
    stats = {
        'total_routes': len(routes_info),
        'admin_routes': len([r for r in routes_info if r['is_admin_route']]),
        'auth_routes': len([r for r in routes_info if r['is_auth_route']]),
        'main_routes': len([r for r in routes_info if r['is_main_route']]),
        'other_routes': len([r for r in routes_info if not any([r['is_admin_route'], r['is_auth_route'], r['is_main_route']])])
    }
    
    return {
        'routes': routes_info,
        'statistics': stats,
        'route_groups': {
            'frontend': [r for r in routes_info if r['is_main_route']],
            'auth': [r for r in routes_info if r['is_auth_route']],
            'admin': [r for r in routes_info if r['is_admin_route']],
            'other': [r for r in routes_info if not any([r['is_admin_route'], r['is_auth_route'], r['is_main_route']])]
        }
    }