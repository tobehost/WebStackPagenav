#!/usr/bin/env python3
"""
初始化数据库并可选创建默认管理员用户。
用法:
  ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=secret .venv/bin/python3 scripts/init_db.py
如果未提供环境变量，脚本会使用安全提示并在控制台输出警告（仅用于开发/演示）。
"""
import os
import sys
import getpass

# Ensure project root is on sys.path when script is executed from scripts/ so
# we can import the 'app' package.
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from app.app import create_app
from app.models import db, User


def main():
    # 读取环境变量或使用默认值（开发时方便，生产请务必通过 env 传入）
    username = os.environ.get('ADMIN_USERNAME')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')

    if not username:
        username = input('管理员用户名 (默认: admin): ') or 'admin'
    if not email:
        email = input('管理员邮箱 (默认: admin@example.com): ') or 'admin@example.com'
    if not password:
        # 如果终端可用，使用隐藏输入；否则回退到明文输入
        try:
            password = getpass.getpass('管理员密码 (留空将使用 "admin"，仅用于本地开发): ')
        except Exception:
            password = input('管理员密码 (留空将使用 "admin"，仅用于本地开发): ')
        if not password:
            password = 'admin'
            print('警告：使用默认密码 admin —— 仅用于开发环境，请尽快修改。')

    # 在初始化脚本中跳过 admin 初始化以避免在模型/表单创建阶段触发 flask-admin 的元数据检查
    app = create_app(init_admin=False)
    with app.app_context():
        print('创建数据库表...')
        db.create_all()

        user = User.query.filter_by(username=username).first()
        if user:
            print(f"用户 {username} 已存在，跳过创建。")
        else:
            user = User(username=username, email=email, is_admin=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"已创建管理员用户: {username} ({email})")


if __name__ == '__main__':
    main()
