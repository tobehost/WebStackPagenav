#!/usr/bin/env bash

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 显示帮助信息
show_help() {
    echo -e "${BLUE}WebStackPagenav 启动脚本${NC}"
    echo
    echo "用法: $0 [选项]"
    echo
    echo "选项:"
    echo "  -e, --env [dev|prod]    指定运行环境 (默认: dev)"
    echo "  -p, --port PORT         指定端口号 (默认: 5000)"
    echo "  -h, --host HOST         指定主机地址 (默认: 127.0.0.1)"
    echo "  --init-db              初始化/重置数据库"
    echo "  -h, --help             显示此帮助信息"
    echo
    echo "示例:"
    echo "  $0 --env dev           以开发模式运行"
    echo "  $0 --env prod --port 8000   以生产模式运行在端口 8000"
    echo "  $0 --init-db          初始化数据库"
}

# 初始化默认值
ENV="dev"
PORT="5000"
HOST="127.0.0.1"
INIT_DB="false"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENV="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --init-db)
            INIT_DB="true"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查运行环境
if [[ "$ENV" != "dev" && "$ENV" != "prod" ]]; then
    echo -e "${RED}错误: 环境必须是 'dev' 或 'prod'${NC}"
    exit 1
fi

# 确保在项目根目录
cd "$PROJECT_ROOT" || exit 1

# 创建/激活虚拟环境
echo -e "${BLUE}=== 检查 Python 虚拟环境 ===${NC}"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}创建新的虚拟环境...${NC}"
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo -e "${BLUE}=== 安装项目依赖 ===${NC}"
pip install -r requirements.txt

# 设置环境变量
export FLASK_APP="app.app"
export FLASK_ENV="$ENV"
if [ "$ENV" = "prod" ]; then
    export FLASK_DEBUG=0
else
    export FLASK_DEBUG=1
fi

# 如果存在 .env 文件，加载它
if [ -f ".env" ]; then
    echo -e "${GREEN}加载 .env 文件中的环境变量${NC}"
    set -a
    source .env
    set +a
fi

# 初始化数据库（如果需要）
if [ "$INIT_DB" = "true" ]; then
    echo -e "${BLUE}=== 初始化数据库 ===${NC}"
    python scripts/init_db.py
fi

# 启动应用
echo -e "${BLUE}=== 启动应用 ===${NC}"
echo -e "环境: ${GREEN}$ENV${NC}"
echo -e "地址: ${GREEN}http://$HOST:$PORT${NC}"

if [ "$ENV" = "prod" ]; then
    # 生产环境使用 gunicorn
    echo -e "${YELLOW}使用 gunicorn 启动生产服务器...${NC}"
    gunicorn -w 4 -b "$HOST:$PORT" "app:app"
else
    # 开发环境使用 Flask 开发服务器
    echo -e "${YELLOW}使用 Flask 开发服务器启动...${NC}"
    flask run --host="$HOST" --port="$PORT"
fi