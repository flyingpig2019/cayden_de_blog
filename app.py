import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from urllib.parse import quote

app = Flask(__name__, static_folder='static', template_folder='.')

# 确保数据库目录存在
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'guestbook.db')

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 路由：静态文件
@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return app.send_static_file(path)

# 路由：主页
@app.route('/')
def index():
    return render_template('index.html')

# 路由：留言板页面
@app.route('/guestbook.html')
def guestbook():
    return render_template('guestbook.html')

# API：获取所有留言
@app.route('/api/messages', methods=['GET'])
def get_messages():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(messages)

# API：添加新留言
@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.json
    
    # 验证数据
    if not all(key in data for key in ['name', 'email', 'message']):
        return jsonify({'error': '缺少必要字段'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
        (data['name'], data['email'], data['message'])
    )
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': message_id, 'success': True}), 201

if __name__ == '__main__':
    app.run(debug=True, port=8000)