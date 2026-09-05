import threading
import time
import requests
from server import start_server

# Start server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(2)

# Test APIs
print('Testing /api/learner-profile...')
r = requests.get('http://localhost:8050/api/learner-profile')
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Has skill_gaps:', 'skill_gaps' in data)
    print('Has domain_scores:', 'domain_scores' in data)

print('Testing /api/recommendations...')
r = requests.get('http://localhost:8050/api/recommendations')
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Has learning_pathway:', 'learning_pathway' in data)
    if 'learning_pathway' in data:
        for k, v in data['learning_pathway'].items():
            print(f'  {k}: {len(v)} courses')

print('Testing /api/igot/courses...')
r = requests.get('http://localhost:8050/api/igot/courses')
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Total iGOT courses:', len(data))

print('Testing /api/nssta/programmes...')
r = requests.get('http://localhost:8050/api/nssta/programmes')
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Total NSSTA programmes:', len(data))

print('Testing /api/materials...')
r = requests.get('http://localhost:8050/api/materials')
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Total materials:', len(data))

print('Testing /api/assessments...')
r = requests.get('http://localhost:8050/api/assessments')
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Total assessments:', len(data))