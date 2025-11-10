我已经查看了仓库中与 Cloudflare 隧道部署相关的文件（cloudflared 配置、systemd 服务、文档），接下来我会把检查结果、所需前置条件和一个可直接使用的 GitHub Actions 部署建议列出来，并说明需要在 GitHub 中设置哪些 Secrets。如果你愿意，我之后可以把示例 workflow 提交到仓库（需你确认）。现在我把第 1 项标记为完成并将下一步（列出前置条件）设为进行中。

正在启动(2/5) 列出需要的 Cloudflare 前置条件

## 一、仓库中我已经检查到的相关文件（要点）
- config.yml（你仓库内已有）：
    - 内容使用变量形式：tunnel: $TUNNEL_ID，credentials-file: /root/.cloudflared/$TUNNEL_ID.json
    - ingress 将 hostname nav.apescope.com 映射到 http://localhost:5000
    - 说明：仓库已经有一个合适的 ingress 配置范例，适合部署在运行 Flask（gunicorn）且监听 5000 的服务器上。

- navpage.service（仓库根）：
    -  systemd 服务配置，WorkingDirectory 指向 /opt/navpage，ExecStart 使用 gunicorn 启动 app:app，适合放在目标服务器的 navpage.service 并启用。

- cloudflare-deploy.md：
    - 仓库已包含一份较完整的部署方案示例（包括多种可选方案：SSH 部署、Docker、GitHub Actions），可以直接借鉴。

- 其他：
    - main.py、requirements.txt、app 等已经存在，说明应用可作为普通 Python/gunicorn 服务部署。

**结论**：仓库已经包含了 server-side 部署所需的关键配置（cloudflared 的 config.yml 模板、systemd service），这意味着推荐把 Cloudflare Tunnel 作为在目标服务器上长期运行的服务来使用（也可以通过 GitHub Actions 触发远程部署并重启服务）。

## 二、部署到 Cloudflare Tunnel 的两种常见模式（优劣）

1. 推荐（稳定、生产化）：在你的服务器上长期运行 Cloudflared 隧道（systemd 管理），GitHub Actions 负责把代码部署/更新到服务器并重启 systemd 服务。

    - 优点：安全、稳定、凭证（credentials file）仅存服务器，不暴露在 CI 日志中。
    - 你仓库已有 navpage.service 与 config.yml，很适合此方案。

2. 另一选项（临时/测试）：在 GitHub Actions runner 上临时启动 cloudflared 隧道（使用 token）并在 runner 上运行应用。

    - 缺点：CI runner 是短暂的（短期暴露），不适合长期/生产；需要在 Actions 中管理隧道 token 或 credentials，风险较高。
    - 只建议用于临时演示或调试。

我会以方案 1（在服务器运行隧道、用 Actions 部署代码）为主线给出具体步骤和示例。

## 三、前置条件（你需要在开始前准备/确认的事项）

1. Cloudflare 相关
    - 你必须有一个 Cloudflare 账号，并且你的域名（例如 apescope.com）已经添加到该账号，并正确设置了 Cloudflare 的 nameservers。
    - 访问 Cloudflare Dashboard → Zero Trust → Access → Tunnels（或 Cloudflare Tunnels 区域）。

2. 在 Cloudflare 创建 Tunnel（两种获取凭证方式）
    - 推荐（服务器长期运行）：在目标服务器或本地使用 cloudflared CLI 运行：
        - 安装 cloudflared（见下面命令示例）
        - 执行：cloudflared tunnel create <NAME>
            - 该命令会返回一个 tunnel id（UUID）并在 ~/.cloudflared/<TUNNEL_ID>.json 生成凭证文件（credentials file）。
        - 然后你可以运行：cloudflared tunnel route dns <TUNNEL_ID> nav.apescope.com
            - 这会在 Cloudflare 中为你的隧道创建 DNS 记录（如果你有 API 权限），或者你可以在 Dashboard 手动创建 CNAME/route。
    - 可选（token，用于临时/CI）：在 Cloudflare Dashboard 创建一个短期运行的 token（或使用 cloudflared 生成 token），token 可用于在没有本地持久凭证文件的场景下运行 cloudflared tunnel --token <TOKEN> run。注意：token 的安全性和生命周期需谨慎管理。

3. 目标服务器准备（推荐放置在 /opt/navpage）

    - 一个公网可连的服务器（或私有服务器，通过 Cloudflare 隧道暴露），SSH 可以登录。
    -在服务器上安装 Python（与你项目兼容的版本）、pip、virtualenv；安装并配置 gunicorn（navpage.service 中配置了 gunicorn）。
    - 在服务器上安装 cloudflared 并将凭证文件放到 /root/.cloudflared/<TUNNEL_ID>.json（或更新 config.yml 的 credentials-file 路径使其指向凭证位置）。
    - 将 config.yml 放到 config.yml（或你希望的位置），并把 $TUNNEL_ID 替换为实际 tunnel id，或在运行时通过 env var 注入。

4. GitHub 侧准备（用于自动部署）
    - 在 GitHub 仓库的 Settings → Secrets 添加至少：
        - SERVER_HOST（服务器 IP 或域名）
        - SERVER_USER（SSH 用户）
        -SERVER_SSH_KEY（用于 SSH 的私钥，注意权限）
        - 可选：SERVER_SSH_PORT（如果非 22）

    - 不建议把 Cloudflare 隧道的长期凭证文件放入 GitHub Secrets 并在 Actions 中暴露；最好把凭证直接保存在目标服务器上（/root/.cloudflared）并由 Actions 仅触发代码更新与 systemd 重启。

## 四、在服务器上手工完成 Tunnel 的快速步骤（示例）
（在服务器上执行）

1. 安装 cloudflared（Linux x86_64 示例）
---bash
wget -q -O /tmp/cloudflared-linux-amd64 https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64sudo mv /tmp/cloudflared-linux-amd64 /usr/local/bin/cloudflaredsudo chmod +x /usr/local/bin/cloudflared
---

2. 在服务器上创建隧道并获取凭证文件（推荐）
---bash
# 在目标服务器（root 或具有写入 ~/.cloudflared 的用户）：cloudflared tunnel create my-navpage-tunnel# 输出会包含 TUNNEL ID（uuid），并在 ~/.cloudflared/<TUNNEL_ID>.json 写入凭证
---

3. 为你的主机名创建 DNS 路由（两种方式）

- 自动（如果你使用 cloudflared 命令并且该账户有权限）：
---bash
cloudflared tunnel route dns <TUNNEL_ID> nav.apescope.com
---

- 或者在 Cloudflare Dashboard → Tunnels 手动添加主机名并映射到隧道。

4. 将仓库复制到服务器并配置（假设放在 /opt/navpage）
---bash
sudo mkdir -p /opt/navpagesudo chown $USER:$USER /opt/navpagecd /opt/navpagegit clone <your-repo-url> .  # 或 git pullpython3 -m venv .venvsource .venv/bin/activatepip install -r requirements.txt
---

5. 配置 cloudflared 的 config（举例）

- 编辑仓库中的 config.yml，将 tunnel: $TUNNEL_ID 更改为实际的 tunnel id（或在运行时通过 env 注入）。
- 确保 credentials-file 指向实际的凭证文件（例如 /root/.cloudflared/<TUNNEL_ID>.json）。

6. 将 `navpage.service` 拷贝并启用 systemd：
---bash
sudo cp navpage.service /etc/systemd/system/navpage.servicesudo systemctl daemon-reloadsudo systemctl enable navpage.servicesudo systemctl start navpage.service
---

7. 运行 Cloudflared 隧道（systemd 或直接 run）

- 直接运行（测试用）：
---bash
# 若已在 ~/.cloudflared 有凭证，且 config 指定正确cloudflared --config /opt/navpage/cloudflared-config/config.yml tunnel run# 或使用 name:cloudflared tunnel run my-navpage-tunnel
---

- 建议把 cloudflared 也作为 systemd 服务（cloudflared 官方有示例 systemd 单元），并配置好 --config 或 --credentials-file，确保重启后自动运行。

## 五、推荐的 GitHub Actions（示例：SSH 部署并重启服务）
说明：该示例不把隧道凭证放到 Actions 中，只在服务器上持久保存凭证。Actions 仅负责把最新代码拉到服务器、安装依赖并重启 systemd 服务。

在仓库中创建 deploy.yml（示例）：

（摘要说明）

- 触发：push 到 main/master
- 步骤：checkout → ssh 到服务器并执行拉取/安装/重启命令
- 需要的 GitHub Secrets：SERVER_HOST、SERVER_USER、SERVER_SSH_KEY（也可添加 SERVER_SSH_PORT）

示例 workflow（你可以按需调整 python 版本、虚拟环境路径、workdir）：

---yaml

name: Deploy to Server (SSH)
on:  
    push:    
        branches: [ main,master ]
        
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout
          uses: actions/checkout@v4
    
        - name: Deploy via SSH
          uses: appleboy/ssh-action@v1
          with:
            host: ${{ secrets.SERVER_HOST }}
            username: ${{ secrets.SERVER_USER }}
            key: ${{ secrets.SERVER_SSH_KEY }}
            port: ${{ secrets.SERVER_SSH_PORT || 22 }}
            script: |
              set -e
              cd /opt/navpage
              git fetch --all
              git reset --hard $GITHUB_SHA
              # Activate venv and install dependencies
              python3 -m venv .venv || true
              source .venv/bin/activate
              pip install -r requirements.txt
              # Optional: run migrations / init script
              # python scripts/init_db.py --non-interactive ...          # Restart app service
              sudo systemctl restart navpage.service
              # Restart cloudflared (如果你把 cloudflared 写成了 systemd 服务)
              sudo systemctl restart cloudflared || true
---
注意事项：

- appleboy/ssh-action 会通过 SSH 执行命令。确保 SERVER_SSH_KEY 对应的公钥已经被加入到目标服务器的 ~/.ssh/authorized_keys。
- 仅把 SSH 私钥 存入 GitHub Secrets（不可在 Action 输出日志中打印该私钥）。
- 如果你确实需要在 Actions 中传送 cloudflared 的凭证文件（不推荐），请把凭证作为 Secret（极不推荐把大 JSON 直接做 Secret），并在 Action 中以私密方式将其写入 /root/.cloudflared/...。但更安全的做法是手动在服务器上完成 tunnel 创建与凭证保存。

## 六、需要在 Cloudflare 侧手动或在服务器执行的关键操作（总结）
1. 在 Cloudflare Dashboard 或 cloudflared CLI 创建 Tunnel，拿到 Tunnel ID 与 credentials json 文件（推荐）。
2. 在 Cloudflare 中把主机名（nav.apescope.com）路由到该隧道（通过 cloudflared tunnel route dns 或 Dashboard）。
3. 在服务器上把凭证放到 /root/.cloudflared/<TUNNEL_ID>.json，并把 config.yml 中的 tunnel、credentials-file 更新对应值（你的仓库文件已经有模板）。
4. 把应用代码放到服务器（/opt/navpage），虚拟环境、pip install，启用 navpage.service 并启动。
5. 启动 cloudflared 隧道（最好用 systemd 管理），确认 nav.apescope.com 能访问并正确转发到本地 5000。

## 七、需要在 GitHub 仓库中配置的 Secrets（推荐）
- SERVER_HOST — 目标服务器 IP/域名
- SERVER_USER — SSH 登录用户名
- SERVER_SSH_KEY — SSH 私钥（对应服务器上已添加的公钥）
- SERVER_SSH_PORT —（可选）SSH 端口，默认 22

（可选，不建议）：
- CF_TUNNEL_TOKEN — 如你选择在 CI 中运行 cloudflared（短期 token），可放此 Secret（风险较高）
- CF_CREDENTIAL_JSON — 强烈不推荐；若确实需要，需非常谨慎并考虑自动清理

## 八、我可以为你继续做的事（你可以选择其中一项）
- A）我把上面示例的 deploy.yml 加入仓库并提交（需要你确认并允许我编辑仓库文件）。
- B）我把 cloudflared 的 systemd 单元示例和一个 server-side 安装脚本（在 scripts 下）加入仓库，便于在服务器上执行一次性安装。
- C）我生成一份更严格的“在 Cloudflare Dashboard 创建 token / tunnel”详细步骤文档（含截图/命令），并把你仓库的 config.yml 用实际 TUNNEL_ID 填充（如果你把凭证放为 GitHub Secret，我可以示例如何在 Actions 中安全写入凭证文件——但不推荐）。
- D）仅给你一个最终的“部署检查清单”以便你手动执行（不改动仓库）。

请告诉我你想要我继续做哪一项（A/B/C/D），或者直接让我把示例 workflow 添加到仓库并提交（会在仓库创建 deploy.yml 并提交一次修改）。

**我已经更新了工作流文件，主要改进包括：**

1. 简化流程：移除了 Docker 相关步骤，专注于 Python 应用部署
2. 使用最新的 Python 3.12（与你的本地开发环境一致）
3. 改进部署脚本：
    - 添加错误处理（set -e）
    - 使用 git reset --hard 确保代码完全同步
    - 正确管理 Python 虚拟环境
    - 添加服务状态检查和日志输出
    - 在服务重启后添加短暂延迟以等待启动
4. 本地化：添加了中文注释和输出信息
5. 添加 workflow_dispatch 触发器支持手动运行
6. 统一 secrets 命名（SERVER_USER 而不是 SERVER_USERNAME）

要使用这个工作流，你需要在 GitHub 仓库的 Settings → Secrets and variables → Actions 中添加以下 secrets：

1. SERVER_HOST: 你的服务器 IP 或域名
2. SERVER_USER: SSH 登录用户名
3. SERVER_SSH_KEY: SSH 私钥（确保对应的公钥已添加到服务器的 authorized_keys）
4. SERVER_SSH_PORT（可选）: SSH 端口，如果不是默认的 22

工作流会在：

- 推送到 main 或 master 分支时自动运行
- 可以在 GitHub Actions 页面手动触发
- 先运行测试，测试通过才会部署
- 部署时会显示详细的进度和服务状态

**需要注意的是**：

1. 确保服务器上的 /opt/navpage 目录存在且有正确的权限
2. 确保已经在服务器上正确配置了 navpage.service 和 cloudflared
3. 部署用户需要有 sudo 权限来重启服务

你想让我展示如何在 GitHub 上配置这些 secrets 吗？或者需要我解释工作流中的某些具体部分？