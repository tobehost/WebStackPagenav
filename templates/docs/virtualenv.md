# 在本项目中创建 Python 虚拟环境（简明指南）

1. 检查 Python：
   - python3 --version

2. 在项目根目录创建虚拟环境（推荐目录：.venv）：
   - python3 -m venv .venv

3. 激活虚拟环境：
   - Linux / macOS:
     - source .venv/bin/activate
   - Windows (PowerShell):
     - .venv\Scripts\Activate.ps1
   - Windows (cmd):
     - .venv\Scripts\activate.bat

4. 更新 pip 并安装依赖：
   - pip install --upgrade pip
   - 如果项目有 requirements.txt：
     - pip install -r requirements.txt
   - 否则安装需要的包，例如：
     - pip install flask

5. 将已安装的依赖锁定到 requirements.txt：
   - pip freeze > requirements.txt

6. 退出虚拟环境：
   - deactivate

7. 推荐把虚拟环境目录加入 .gitignore：
   - 在 .gitignore 中添加一行： .venv/

附注：
- 在容器 / devcontainer 中，激活虚拟环境仍需在交互 shell 中执行 source 命令。
- 如果需要更高级的依赖/环境管理，可考虑使用 pipx / pip-tools / poetry / pyenv 等工具。
