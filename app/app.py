# app.py
"""
此文件仅作为应用入口点，所有功能已移至相应模块：
- 应用工厂: app/__init__.py
- 主路由: app/routes/main.py
- 认证路由: app/routes/auth.py
- 数据中台: app/admin/views/
"""

from . import create_app

# 如果直接运行此文件（仅用于开发环境）
if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)