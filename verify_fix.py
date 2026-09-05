import threading
import time
import requests
import sys

def run_server():
    from server import start_server
    start_server()

# Start server in background thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(3)

print('Testing APIs...')
endpoints = ['/api/learner-profile', '/api/recommendations', '/api/framework', '/api/admin/analytics']
for ep in endpoints:
    try:
        r = requests.get('http://localhost:8050' + ep, timeout=5)
        print(f'{ep}: Status {r.status_code}')
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict):
                print(f'  Keys: {list(data.keys())}')
            elif isinstance(data, list):
                print(f'  Items: {len(data)}')
    except Exception as e:
        print(f'{ep}: Exception: {e}')

print('Done')