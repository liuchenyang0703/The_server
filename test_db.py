from server import app, db, ServerPassword

with app.app_context():
    # 测试数据库连接
    try:
        # 检查ServerPassword表是否存在
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"数据库中存在的表: {tables}")
        
        # 如果表存在，尝试查询数据
        if 'server_password' in tables:
            passwords = ServerPassword.query.all()
            print(f"查询到的密码数量: {len(passwords)}")
            for password in passwords:
                print(f"ID: {password.id}, 内网IP: {password.inner_ip}")
        else:
            print("server_password表不存在")
            
        # 尝试添加一条测试数据
        test_password = ServerPassword(
            inner_ip='192.168.1.100',
            port='22',
            username='testuser',
            user_password='testpass',
            root_password='rootpass',
            outer_ip='10.0.0.100'
        )
        db.session.add(test_password)
        db.session.commit()
        print("成功添加测试数据")
        
        # 再次查询数据
        passwords = ServerPassword.query.all()
        print(f"添加后查询到的密码数量: {len(passwords)}")
        
    except Exception as e:
        print(f"数据库操作失败: {e}")
        db.session.rollback()