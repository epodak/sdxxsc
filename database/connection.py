import os
import sqlite3
from utils.decorators import print_log

@print_log()
def get_db_connection():
    """获取数据库连接"""
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    # 连接数据库
    conn = sqlite3.connect('data/products.db')
    conn.row_factory = sqlite3.Row
    return conn 