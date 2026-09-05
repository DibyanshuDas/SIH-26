import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)

users_to_create = [
    {"email": "admin@mospi.gov.in", "password": "123456", "display_name": "Cadre Admin"},
    {"email": "officer@mospi.gov.in", "password": "123456", "display_name": "Standard Officer"}
]

for user_data in users_to_create:
    try:
        user = auth.create_user(
            email=user_data['email'],
            password=user_data['password'],
            display_name=user_data['display_name']
        )
        print(f"Successfully created new user: {user.uid} ({user.email})")
    except Exception as e:
        print(f"Error creating user {user_data['email']}: {e}")
