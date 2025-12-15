# 服务器管理系统

## 项目介绍

> 这是一个基于Flask框架开发的服务器管理系统，用于管理服务器信息和密码，提供管理员后台和用户查询功能。

## 项目结构

```
.
├── check_admin.py          # 管理员用户检查与创建脚本
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
│   │   ├── edit_server.html        # 编辑服务器页面
│   │   ├── login.html              # 登录页面
│   │   ├── password_admin.html     # 密码管理页面
│   │   └── server_admin.html       # 服务器管理页面
│   └── index.html          # 首页，用于查询服务器信息
├── test_db.py              # 数据库测试脚本
└── the_server.sql          # 数据库结构文件
```

## 主要功能

### 1. 用户认证
- 管理员登录系统
- 用户权限管理

### 2. 服务器信息管理
- 添加新服务器信息
- 编辑服务器信息
- 删除服务器信息
- 查看服务器列表

### 3. 服务器密码管理
- 添加服务器密码
- 编辑服务器密码
- 删除服务器密码
- 查看服务器密码列表

### 4. 服务器查询
- 通过首页查询服务器信息

### 5. 管理员后台
- 管理员仪表盘
- 密码修改功能

## 技术栈

- **编程语言**: Python 3.6+
- **后端框架**: Flask
- **数据库**: MySQL (使用SQLAlchemy ORM)
- **前端**: HTML, CSS, JavaScript, Bootstrap
- **其他**: Flask-SQLAlchemy, pymysql

## 安装与运行

### 1. 安装依赖

```bash
pip install flask_sqlalchemy flask pymysql -i https://mirrors.aliyun.com/pypi/simple/
```

### 2. 数据库配置

在`server.py`中配置数据库连接信息：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
```

### 3. 初始化数据库

```bash
# 运行服务器，自动创建数据库表
python3 server.py
```

或导入SQL文件：

```bash
mysql -u username -p dbname < the_server.sql
```

### 4. 创建管理员用户

运行以下脚本创建管理员用户：

```bash
python check_admin.py
```

默认管理员账号：
- 用户名: admin
- 密码: admin123

### 5. 启动应用

```bash
python server.py
```

访问 `http://localhost:5000` 查看首页
访问 `http://localhost:5000/admin` 进入管理员后台

## 测试数据库

运行以下脚本测试数据库连接和操作：

```bash
python test_db.py
```

## 注意事项

1. 请确保在生产环境中修改默认管理员密码
2. 建议使用HTTPS协议部署应用
3. 定期备份数据库

## 许可证

MIT License