# 服务器管理系统

## 项目介绍

这是一个基于 Flask 的服务器管理系统，用于管理服务器信息和服务器密码，提供管理员后台、用户查询、邮件通知和企业微信机器人通知。

## 项目结构

```text
.
├── check_admin.py          # 管理员用户检查与创建脚本
├── email_config.py         # 邮件通知配置与发送逻辑
├── wechat_config.py        # 企业微信机器人通知配置与发送逻辑
├── README.md               # 项目说明文档
├── server.py               # 主应用程序文件
├── static/                 # 静态资源目录
│   ├── css/                # CSS样式文件
│   │   ├── 404-bootstrap.min.css   # 404错误页面样式
│   │   ├── 404-style.css           # 404错误页面样式
│   │   ├── bootstrap.min.css       # Bootstrap样式
│   │   └── sidebar.css             # 侧边栏样式
│   ├── img/                # 图片资源
│   └── js/                 # JavaScript文件
│       ├── 404-gsap.min.js         # 404错误页面动画脚本
│       ├── 404-script.js           # 404错误页面脚本
│       └── bootstrap.bundle.min.js # Bootstrap脚本
├── templates/              # HTML模板文件
│   ├── 404.html            # 404错误页面
│   ├── admin/              # 管理员后台页面
│   │   ├── add_password.html       # 添加服务器密码页面
│   │   ├── add_server.html         # 添加服务器页面
│   │   ├── admin_dashboard.html    # 管理员仪表盘页面
│   │   ├── admin_layout.html       # 管理员布局页面
│   │   ├── change_password.html    # 密码修改页面    
│   │   ├── delete_confirm.html     # 删除确认页面
│   │   ├── edit_password.html      # 编辑密码页面
│   │   ├── edit_server.html        # 编辑服务器页面
│   │   ├── login.html              # 登录页面
│   │   ├── password_admin.html     # 密码管理页面
│   │   └── server_admin.html       # 服务器管理页面
│   └── index.html          # 首页，用于查询服务器信息
├── test_db.py              # 数据库测试脚本
└── the_server.sql          # 数据库结构文件
```



## 主要功能

### 1. 用户使用层面 - 查询

* 查询服务器配置信息
* 查询服务器密码信息

### 2. 用户认证

- 管理员登录系统
- 用户权限管理

### 3. 服务器信息管理

- 添加新服务器信息
- 编辑服务器信息
- 删除服务器信息
- 查看服务器列表

### 4. 服务器密码管理

- 添加服务器密码
- 编辑服务器密码
- 删除服务器密码
- 查看服务器密码列表

### 5. 管理员后台

- 管理员仪表盘
- 密码修改功能

### 6. 邮件、企业微信通知告警

- 服务器信息管理操作（增删改）邮件告警
- 服务器密码管理操作（增删改）邮件告警
- 异步通知，不影响操作响应速度
- 支持邮件通知和企业微信机器人通知，可分别开关

## 技术栈

- **编程语言**: Python 3.8+
- **后端框架**: Flask
- **数据库**: MySQL (使用SQLAlchemy ORM)
- **前端**: HTML, CSS, JavaScript, Bootstrap
- **其他**: Flask-SQLAlchemy, pymysql, smtplib
- **通知**：邮件、企业微信



## 安装与运行

### 1. 安装依赖

> 请提前安装好python环境及pip环境，python版本需要使用3.8及以上；

```bash
pip3 install flask_sqlalchemy flask pymysql -i https://mirrors.aliyun.com/pypi/simple/
```

### 2. 数据库配置

在 `server.py` 中配置数据库连接信息：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
```

### 3. 通知开关

通知总入口在 `server.py` 中，邮件和企业微信可分别开关：

```python
ENABLE_EMAIL_NOTIFICATION = True
ENABLE_WECHAT_NOTIFICATION = True
```

设置为 `False` 后，对应通知不会发送。

### 4. 邮件配置

在 `email_config.py` 中配置邮件发送信息。当前默认使用 465 SSL 端口，适合云服务器无法使用 25 端口的场景：

```python
# 邮件配置
SMTP_SERVER = 'smtp.163.com'    # SMTP服务器的地址
SMTP_PORT = 465                 # SMTP服务器的端口号
SMTP_USER = 'test@163.com'      # 发件人邮箱（用于登录）
SMTP_PASSWORD = '122222222222'  # 发件人邮箱SMTP授权码
SENDER = 'test@163.com'         # 发件人邮箱（用于发送）
RECIPIENTS = ['shoujianren123@qq.com'] # 收件人邮箱列表，多个可使用“,”分割
```

### 5. 企业微信配置

在 `wechat_config.py` 中配置企业微信机器人 Webhook：

```python
WECHAT_WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key'
```

系统会复用原有邮件通知内容，自动转换为企业微信 Markdown 消息发送。

### 6. 初始化数据库

运行服务时会自动创建表：

```bash
python3 server.py
```

也可以导入 SQL 文件：

```bash
mysql -u username -p dbname < the_server.sql
```

### 7. 创建管理员用户

```bash
python3 check_admin.py
```

默认管理员账号：

- 用户名：`admin`
- 密码：`admin123`

### 8. 启动应用

```bash
python3 server.py
```

访问：

- 首页：`http://localhost:5000`
- 管理员后台：`http://localhost:5000/admin`

## 通知说明

以下操作完成数据库写入后，会通过后台线程异步发送通知，避免阻塞当前请求：

- 新增、更新、删除服务器信息
- 新增、更新、删除服务器密码信息

邮件通知调用 `email_config.py` 中的 `send_email`。

企业微信通知调用 `wechat_config.py` 中的 `send_wechat_notification`。



## 邮件通知格式

### 1. 新增服务器信息

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202601131005540.png)

### 2. 更新服务器信息

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202601131007319.png)

### 3. 删除服务器信息

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202601131007626.png)

### 4. 新增服务器密码信息

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202601131008237.png)

### 5. 更新服务器密码信息

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202601131008805.png)

### 6. 删除服务器密码信息

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202601131009551.png)

## 

## 企业微信通知格式

![](https://gcore.jsdelivr.net/gh/liuchenyang0703/blog-images@main/images/202606121612874.png)

## 注意事项

1. 生产环境请修改默认管理员密码和 `app.secret_key`。
2. 建议使用 HTTPS 部署应用。
3. 请定期备份数据库。
4. 邮箱授权码需要使用 SMTP 授权码，不是登录密码。
5. 如果通知发送失败，请检查网络、防火墙、SMTP 配置和企业微信机器人 Webhook。

## 许可证 && 行为准则

[MIT License](./LICENSE) | [行为准则](./CODE_OF_CONDUCT.md)