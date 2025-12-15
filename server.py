from flask import Flask, render_template, request, jsonify, redirect, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)

# 配置MySQL数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123123@172.16.10.65:3306/The_server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'  # 用于session加密的密钥

db = SQLAlchemy(app)

# 定义服务器信息模型
class ServerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False)
    os = db.Column(db.String(100), nullable=False)
    kernel = db.Column(db.String(100), nullable=False)
    gpu_model = db.Column(db.String(100), nullable=True, default='无显卡')
    gpu_memory = db.Column(db.String(50), nullable=True, default='无显卡')
    ram = db.Column(db.String(50), nullable=False)
    cpu_model = db.Column(db.String(100), nullable=False)
    cpu_cores = db.Column(db.Integer, nullable=False)
    architecture = db.Column(db.String(50), nullable=False)

# 定义服务器密码模型
class ServerPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inner_ip = db.Column(db.String(50), nullable=False)
    port = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=True)
    user_password = db.Column(db.String(100), nullable=True)
    root_password = db.Column(db.String(100), nullable=False)
    outer_ip = db.Column(db.String(200), nullable=True)

# 定义用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' 或 'admin'

# 初始化数据库
with app.app_context():
    db.create_all()

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('admin_dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('login'))  # 使用PRG模式，重定向到GET请求
    return render_template('admin/login.html')

# 登出路由
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 用户登录装饰器
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            # 未登录用户重定向到登录页面
            return redirect(url_for('login'))
        elif session['role'] != 'admin':
            # 已登录但非管理员用户重定向到首页
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# 管理员仪表板
@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

# 修改密码路由
@app.route('/change_password', methods=['GET', 'POST'])
@admin_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        user = User.query.get(session['user_id'])
        
        # 验证原密码（因为数据库中是明文存储的，所以使用明文比较）
        if user.password != old_password:
            flash('原密码错误', 'danger')
        elif new_password != confirm_password:
            flash('两次输入的新密码不一致', 'danger')
        elif new_password == old_password:
            flash('新密码不能与原密码相同', 'danger')
        else:
            user.password = new_password
            db.session.commit()
            flash('密码修改成功，请重新登录', 'success')
            # 清除会话信息
            session.clear()
            return redirect(url_for('login'))
        # 使用PRG模式，重定向到GET请求
        return redirect(url_for('change_password'))
    return render_template('admin/change_password.html')

# 服务器信息后台管理页面
@app.route('/server_admin')
@admin_required
def server_admin():
    return render_template('admin/server_admin.html')

# 服务器密码后台管理页面
@app.route('/password_admin')
@admin_required
def password_admin():
    return render_template('admin/password_admin.html')

# 添加服务器页面
@app.route('/add_server')
@admin_required
def add_server():
    return render_template('admin/add_server.html')

# 添加密码页面
@app.route('/add_password')
@admin_required
def add_password():
    return render_template('admin/add_password.html')

# 编辑服务器页面
@app.route('/edit_server')
@admin_required
def edit_server():
    return render_template('admin/edit_server.html')

# 编辑密码页面
@app.route('/edit_password')
@admin_required
def edit_password():
    return render_template('admin/edit_password.html')

# 删除确认页面
@app.route('/delete')
@admin_required
def delete_confirm():
    return render_template('admin/delete_confirm.html')

# 获取服务器列表
@app.route('/api/servers', methods=['GET'])
def get_servers():
    servers = ServerInfo.query.all()
    server_list = []
    for server in servers:
        server_data = {
            'id': server.id,
            'ip': server.ip,
            'os': server.os,
            'kernel': server.kernel,
            'gpu_model': server.gpu_model,
            'gpu_memory': server.gpu_memory,
            'ram': server.ram,
            'cpu_model': server.cpu_model,
            'cpu_cores': server.cpu_cores,
            'architecture': server.architecture
        }
        server_list.append(server_data)
    return jsonify(server_list)

# 按IP模糊查询服务器
@app.route('/api/servers/search/<path:search_term>', methods=['GET'])
def search_servers(search_term):
    servers = ServerInfo.query.filter(
        ServerInfo.ip.like(f'%{search_term}%')
    ).all()
    server_list = []
    for server in servers:
        server_data = {
            'id': server.id,
            'ip': server.ip,
            'os': server.os,
            'kernel': server.kernel,
            'gpu_model': server.gpu_model,
            'gpu_memory': server.gpu_memory,
            'ram': server.ram,
            'cpu_model': server.cpu_model,
            'cpu_cores': server.cpu_cores,
            'architecture': server.architecture
        }
        server_list.append(server_data)
    return jsonify(server_list)

# 添加服务器
@app.route('/api/servers', methods=['POST'])
def add_server_api():
    data = request.get_json()
    new_server = ServerInfo(
        ip=data['ip'],
        os=data['os'],
        kernel=data['kernel'],
        gpu_model=data['gpu_model'] or '无显卡',
        gpu_memory=data['gpu_memory'] or '无显卡',
        ram=data['ram'],
        cpu_model=data['cpu_model'],
        cpu_cores=data['cpu_cores'],
        architecture=data['architecture']
    )
    db.session.add(new_server)
    db.session.commit()
    return jsonify({'message': '服务器已添加'}), 201

# 获取特定服务器
@app.route('/api/servers/<int:server_id>', methods=['GET'])
def get_server(server_id):
    server = ServerInfo.query.get_or_404(server_id)
    server_data = {
        'id': server.id,
        'ip': server.ip,
        'os': server.os,
        'kernel': server.kernel,
        'gpu_model': server.gpu_model,
        'gpu_memory': server.gpu_memory,
        'ram': server.ram,
        'cpu_model': server.cpu_model,
        'cpu_cores': server.cpu_cores,
        'architecture': server.architecture
    }
    return jsonify(server_data)

# 更新服务器
@app.route('/api/servers/<int:server_id>', methods=['PUT'])
def update_server(server_id):
    server = ServerInfo.query.get_or_404(server_id)
    data = request.get_json()
    
    server.ip = data['ip']
    server.os = data['os']
    server.kernel = data['kernel']
    server.gpu_model = data['gpu_model'] or '无显卡'
    server.gpu_memory = data['gpu_memory'] or '无显卡'
    server.ram = data['ram']
    server.cpu_model = data['cpu_model']
    server.cpu_cores = data['cpu_cores']
    server.architecture = data['architecture']
    
    db.session.commit()
    return jsonify({'message': '服务器信息已更新'})

# 删除服务器
@app.route('/api/servers/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    server = ServerInfo.query.get_or_404(server_id)
    db.session.delete(server)
    db.session.commit()
    return jsonify({'message': '服务器信息已删除'})

# 获取密码列表
@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    try:
        passwords = ServerPassword.query.all()
        print(f"查询到的密码数量: {len(passwords)}")
        password_list = []
        for password in passwords:
            password_data = {
                'id': password.id,
                'inner_ip': password.inner_ip,
                'port': password.port,
                'username': password.username,
                'user_password': password.user_password,
                'root_password': password.root_password,
                'outer_ip': password.outer_ip
            }
            password_list.append(password_data)
        return jsonify(password_list)
    except Exception as e:
        print(f"查询密码列表时出错: {e}")
        return jsonify([]), 500

# 按IP模糊查询密码
@app.route('/api/passwords/search/<path:search_term>', methods=['GET'])
def search_passwords(search_term):
    passwords = ServerPassword.query.filter(
        ServerPassword.inner_ip.like(f'%{search_term}%') | 
        ServerPassword.outer_ip.like(f'%{search_term}%')
    ).all()
    password_list = []
    for password in passwords:
        password_data = {
            'id': password.id,
            'inner_ip': password.inner_ip,
            'port': password.port,
            'username': password.username,
            'user_password': password.user_password,
            'root_password': password.root_password,
            'outer_ip': password.outer_ip
        }
        password_list.append(password_data)
    return jsonify(password_list)

# 添加密码
@app.route('/api/passwords', methods=['POST'])
def add_password_api():
    data = request.json
    new_password = ServerPassword(
        inner_ip=data['inner_ip'],
        port=data['port'],
        username=data.get('username', ''),
        user_password=data.get('user_password', ''),
        root_password=data['root_password'],
        outer_ip=data.get('outer_ip', '')
    )
    db.session.add(new_password)
    db.session.commit()
    return jsonify({'message': '密码已添加', 'id': new_password.id}), 201

# 验证管理员密码的函数
def validate_admin_password(password):
    # 查找管理员用户（这里假设只有一个管理员，且用户名固定为 'admin'）
    admin = User.query.filter_by(username='admin', role='admin').first()
    if not admin:
        return False
    # 验证密码（暂时使用明文比较，后续应改为哈希验证）
    return admin.password == password

# 处理服务器删除请求
@app.route('/delete_server', methods=['POST'])
def delete_server_route():
    data = request.json
    server_id = data.get('id')
    
    # 删除服务器
    server = ServerInfo.query.get_or_404(server_id)
    db.session.delete(server)
    db.session.commit()
    return jsonify({'message': '服务器信息已删除'})

# 处理密码删除请求
@app.route('/delete_password', methods=['POST'])
def delete_password_route():
    data = request.json
    password_id = data.get('id')
    
    # 删除密码
    password = ServerPassword.query.get_or_404(password_id)
    db.session.delete(password)
    db.session.commit()
    return jsonify({'message': '密码信息已删除'})

# 获取特定密码
@app.route('/api/passwords/<int:password_id>', methods=['GET'])
def get_password(password_id):
    password = ServerPassword.query.get_or_404(password_id)
    password_data = {
        'id': password.id,
        'inner_ip': password.inner_ip,
        'port': password.port,
        'username': password.username,
        'user_password': password.user_password,
        'root_password': password.root_password,
        'outer_ip': password.outer_ip
    }
    return jsonify(password_data)

# 更新密码
@app.route('/api/passwords/<int:password_id>', methods=['PUT'])
def update_password(password_id):
    password = ServerPassword.query.get_or_404(password_id)
    data = request.get_json()
    
    password.inner_ip = data['inner_ip']
    password.port = data['port']
    password.username = data.get('username', '')
    password.user_password = data.get('user_password', '')
    password.root_password = data['root_password']
    password.outer_ip = data.get('outer_ip', '')
    
    db.session.commit()
    return jsonify({'message': '密码信息已更新'})

# 删除密码
@app.route('/api/passwords/<int:password_id>', methods=['DELETE'])
def delete_password(password_id):
    password = ServerPassword.query.get_or_404(password_id)
    db.session.delete(password)
    db.session.commit()
    return jsonify({'message': '密码信息已删除'})

# 404错误处理器
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
