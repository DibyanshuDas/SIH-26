import subprocess
import time
import requests
import sys

# Start server
proc = subprocess.Popen([sys.executable, 'server.py'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=r'D:\SIH\101\SIH')

# Wait for server to start
time.sleep(3)

# Read any output so far
output = []
while True:
    line = proc.stdout.readline()
    if not line:
        break
    output.append(line.strip())
    if 'running at' in line:
        break

print('Server output:', output)

# Test APIs
endpoints = ['/api/igot/courses', '/api/nssta/programmes', '/api/materials', '/api/assessments']
for ep in endpoints:
    try:
        r = requests.get('http://localhost:8050' + ep, timeout=5)
        print(f'{ep}: Status {r.status_code}')
        if r.status_code != 200:
            print(f'  Error: {r.text[:200]}')
    except Exception as e:
        print(f'{ep}: Exception: {e}')

# Kill server
proc.terminate()
proc.wait(timeout=2)