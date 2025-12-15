from server import app, db, User

with app.app_context():
    # 检查数据库连接
    try:
        # 检查User表是否存在
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"数据库中存在的表: {tables}")
        
        # 如果User表存在，检查是否有admin用户
        if 'user' in tables:
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print(f"管理员用户存在: {admin_user.username}")
                print(f"密码: {admin_user.password}")
                print(f"角色: {admin_user.role}")
            else:
                print("管理员用户不存在，正在创建...")
                # 创建admin用户
                admin_user = User(
                    username='admin',
                    password='admin123',  # 这里应该使用加密密码，但为了测试暂时使用明文
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()
                print("管理员用户创建成功！")
                print(f"用户名: {admin_user.username}")
                print(f"密码: admin123")
                print(f"角色: {admin_user.role}")
        else:
            print("User表不存在")
            
    except Exception as e:
        print(f"数据库操作失败: {e}")
        db.session.rollback()