# 开发资源|工具|网址导航

这是**渝乐萌·繁星**项目的附属项目，旨在提供项目开发中使用到的开发资源、工具以及后期运维中需要使用的网址导航。

## 开发环境

技术栈：Flask
部署： Cloudflare Workers, Cloudflare Pages, Github Actions

## 数据库初始化

这个仓库包含一个用于初始化数据库和创建默认管理员的脚本：`scripts/init_db.py`。

用法示例（推荐在开发或部署流程中以环境变量传入凭据，而不是在代码中硬编码）：

非交互、从环境变量读取示例：

```bash
ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=yourpassword \
	.venv/bin/python3 scripts/init_db.py
```

交互式示例（会提示输入用户名/邮箱/密码）：

```bash
.venv/bin/python3 scripts/init_db.py
```

安全建议：
- 永远不要把真实密码直接写进源码。生产环境请通过 CI/CD 的 secret 管理或环境变量注入密码。
- 此脚本仅用于初始化或在受控环境中运行；在生产中建议把初始化纳入可审计的部署流程。

更多细节请参见 `scripts/README.md`。

## License

Copyright © 2025 **[nav.apescope.com](https://nav.apescope.com)** Released under the **MIT License**.

> 注：本站开源的目的是大家能够在本站的基础之上有所启发，做出更多新的东西。并不是让大家照搬所有代码。
> 如果你使用这个开源项目，请**注明**本项目开源地址。

Screenshot 📷
---
![](http://www.webstack.cc/assets/images/webstack_banner_cn.png)
![](http://7xnb6x.com1.z0.glb.clouddn.com/webstack-03-Introduction.png)
![](http://7xnb6x.com1.z0.glb.clouddn.com/webstack-04-infomation.png)
![](http://7xnb6x.com1.z0.glb.clouddn.com/webstack-05-production.png)
![](http://7xnb6x.com1.z0.glb.clouddn.com/webstack-06-production2.png)


