# WebStackPagenav 脚本使用指南

此目录包含项目的辅助脚本，用于管理和运行项目。

## start.sh - 项目启动脚本

用于快速启动项目，支持开发和生产环境。

### 基本用法

```bash
# 开发模式启动（默认）
./scripts/start.sh

# 生产模式启动
./scripts/start.sh --env prod

# 指定端口启动
./scripts/start.sh --port 8000

# 初始化数据库并启动
./scripts/start.sh --init-db
```

### 命令行选项

- `-e, --env [dev|prod]`: 指定运行环境（默认：dev）
- `-p, --port PORT`: 指定端口号（默认：5000）
- `--host HOST`: 指定主机地址（默认：127.0.0.1）
- `--init-db`: 初始化/重置数据库
- `-h, --help`: 显示帮助信息

### 运行模式说明

- 开发模式 (`--env dev`)：
  - 使用 Flask 开发服务器
  - 启用调试器和自动重载
  - 适合本地开发
- 生产模式 (`--env prod`)：
  - 使用 gunicorn 作为 WSGI 服务器
  - 多工作进程
  - 禁用调试功能

## init_db.py - 数据库初始化脚本

用于初始化数据库表和创建管理员用户。

### 使用方式

环境变量方式（适合 CI/CD）：
```bash
ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=yourpassword \
  .venv/bin/python3 scripts/init_db.py
```

交互式方式：
```bash
.venv/bin/python3 scripts/init_db.py
```

## 安全建议

1. 不要在代码中硬编码敏感信息（密码等）
2. 生产环境使用环境变量或 secrets 管理敏感配置
3. 定期更新依赖包版本
4. 生产环境建议使用 `--env prod` 启动
