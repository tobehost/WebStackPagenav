# app/app.py
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# setup_venv.sh
#!/usr/bin/env bash
set -euo pipefail
# 创建并初始化虚拟环境脚本
# 用法:
#   chmod +x scripts/setup_venv.sh
#   ./scripts/setup_venv.sh        # 在当前目录创建 .venv 并安装 requirements.txt（若存在）
# 检查 python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 未安装，请先安装 Python 3."
  exit 1
fi

# 创建 venv（如果不存在）
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  echo "虚拟环境已创建: $VENV_DIR"
else
  echo "虚拟环境已存在: $VENV_DIR"
fi

# 提示如何激活（激活必须在交互 shell 中执行）
echo ""
echo "要激活虚拟环境，请运行："
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "然后可以运行："
echo "  pip install --upgrade pip"
echo "  pip install -r requirements.txt    # 如果存在 requirements.txt"