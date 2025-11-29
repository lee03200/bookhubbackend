# create_db.py
import pymysql

# 数据库连接参数
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '12345678'  # 替换成你的 root 密码
DB_NAME = 'bookhub_db'

# 初始化 connection 为 None，避免 NameError
connection = None

try:
    # 连接到 MySQL 服务器（不指定数据库）
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                       "CHARACTER SET utf8mb4 "
                       "COLLATE utf8mb4_unicode_ci;")
        print(f"✅ 数据库 '{DB_NAME}' 创建成功或已存在！")

except Exception as e:
    print(f"❌ 创建数据库失败: {e}")

finally:
    # 安全关闭连接：只有 connection 被成功创建才关闭
    if connection is not None:
        connection.close()
        print("🔌 MySQL 连接已关闭。")