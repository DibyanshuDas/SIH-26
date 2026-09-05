import threading
import time
import requests
from server import start_server

# Start server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(2)

# Test failing APIs with error details
endpoints = ['/api/igot/courses', '/api/nssta/programmes', '/api/materials', '/api/assessments']

for ep in endpoints:
    print(f'Testing {ep}...')
    r = requests.get('http://localhost:8050' + ep)
    print('Status:', r.status_code)
    if r.status_code != 200:
        print('Error:', r.text[:500])
    else:
        data = r.json()
        if isinstance(data, list):
            print('Total items:', len(data))
        elif isinstance(data, dict):
            print('Keys:', list(data.keys()))