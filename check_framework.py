import json
with open(r'D:\SIH\101\SIH\dashboard\data\competency_framework.json') as f:
    data = json.load(f)
print('Keys:', list(data.keys()))
for k, v in data.items():
    print(f'  {k}: domain_id={v.get("domain_id")}, competencies={len(v.get("competencies", []))}')