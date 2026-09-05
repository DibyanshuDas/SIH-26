from app import app
with app.app_context():
    from flask import request
    with app.test_client() as c:
        rv = c.get('/api/recommendations')
        print(rv.get_json())
