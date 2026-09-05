import json
with open(r'D:\SIH\101\SIH\data\official_profiles.json') as f:
    data = json.load(f)

names = [
    'Dr. Rajeshwar Sharma',
    'Dr. Anita Mukherjee', 
    'Sh. Amit Verma',
    'Ms. Priya Nair',
    'Sh. Gaurav Patel',
    'Ms. Ananya Das',
    'Dr. K. S. Reddy',
    'Sh. Vikram Malhotra'
]

for name in names:
    found = [p for p in data if p['name'] == name]
    if found:
        print(f'FOUND: {name} -> {found[0]["officer_id"]} ({found[0]["division_code"]})')
    else:
        print(f'MISSING: {name}')