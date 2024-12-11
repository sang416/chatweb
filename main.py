from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret!'
async_mode = 'threading'
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*", logger=True, engineio_logger=True)

# MySQL 연결
db_config = {
    'host': 'sang416.mysql.pythonanywhere-services.com',
    'user': 'sang416',
    'password': 'sg13151447',
    'database': 'sang416$default'
}

# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'sg1315',
#     'database': 'chatweb'
# }

# 데이터베이스 초기화
def initialize_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nickname VARCHAR(50) NOT NULL,
            ip_address VARCHAR(50) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

initialize_database()

# 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 웹소켓 메시지 처리
@socketio.on('message')
def handle_message(data):
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    nickname = data.get('nickname', 'Anonymous')
    message = data.get('message', '')

    # 데이터베이스에 메시지 저장
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = '''
        INSERT INTO chat_messages (nickname, ip_address, message, timestamp)
        VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(query, (nickname, ip_address, message, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

    # 클라이언트로 메시지 전송
    send({'nickname': nickname, 'message': message, 'timestamp': datetime.now().strftime('%H:%M:%S')}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
