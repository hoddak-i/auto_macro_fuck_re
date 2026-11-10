import os
import time
import threading
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', '')
messages = []
next_id = 1
lock = threading.Lock()
MAX_MESSAGES = 200

@app.get('/health')
def health():
    return jsonify({'ok': True})

@app.post('/send')
def send_message():
    global next_id
    if not ADMIN_TOKEN:
        return jsonify({'error': 'ADMIN_TOKEN is not configured'}), 503
    supplied = request.headers.get('X-Admin-Token', '')
    if supplied != ADMIN_TOKEN:
        abort(401)
    data = request.get_json(silent=True) or {}
    message = str(data.get('message', '')).strip()
    if not message:
        return jsonify({'error': '메시지를 입력하세요.'}), 400
    if len(message) > 300:
        return jsonify({'error': '메시지는 300자 이하로 입력하세요.'}), 400
    with lock:
        item = {'id': next_id, 'message': message, 'created_at': int(time.time())}
        next_id += 1
        messages.append(item)
        del messages[:-MAX_MESSAGES]
    return jsonify({'ok': True, 'id': item['id']})

@app.get('/messages')
def get_messages():
    try:
        after_id = max(0, int(request.args.get('after', '0')))
    except ValueError:
        return jsonify({'error': '잘못된 after 값'}), 400
    with lock:
        result = [m for m in messages if m['id'] > after_id]
    return jsonify({'messages': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '10000'))
    app.run(host='0.0.0.0', port=port)
