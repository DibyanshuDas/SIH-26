import threading
import time
import requests
import sys
import os

# Add current dir to path
sys.path.insert(0, r'D:\SIH\101\SIH')

def run_server():
    from server import start_server
    start_server()

# Start server in background thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(3)

print('Testing APIs...')
endpoints = ['/api/igot/courses', '/api/nssta/programmes', '/api/materials', '/api/assessments']
for ep in endpoints:
    try:
        r = requests.get('http://localhost:8050' + ep, timeout=5)
        print(f'{ep}: Status {r.status_code}')
        if r.status_code != 200:
            print(f'  Error: {r.text[:300]}')
        else:
            data = r.json()
            if isinstance(data, list):
                print(f'  Items: {len(data)}')
            elif isinstance(data, dict):
                print(f'  Keys: {list(data.keys())}')
    except Exception as e:
        print(f'{ep}: Exception: {e}')

print('Done')