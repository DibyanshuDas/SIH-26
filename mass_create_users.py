import firebase_admin
from firebase_admin import credentials, auth
import json
import os

# Initialize Firebase
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)

# Delete mock officer if exists
try:
    user = auth.get_user_by_email('officer@mospi.gov.in')
    auth.delete_user(user.uid)
    print("Deleted mock officer@mospi.gov.in")
except Exception as e:
    print("Mock officer already deleted or not found.")

# Process 100 profiles
profiles_path = 'data/official_profiles.json'
with open(profiles_path, 'r') as f:
    profiles = json.load(f)

print(f"Loaded {len(profiles)} profiles.")

# We want to create safe emails.
# e.g., name "Dr. Rajeshwar Sharma" -> "rajeshwar.sharma.iss@mospi.gov.in"
# A simpler, guaranteed unique way is to use their ID: OFF-ISS-0 -> off_iss_0@mospi.gov.in
# We will combine name and ID for uniqueness.
import re

def generate_email(name, officer_id):
    clean_name = re.sub(r'[^a-zA-Z]', '', name.split()[0].lower())
    clean_id = officer_id.lower().replace('-', '_')
    return f"{clean_name}.{clean_id}@mospi.gov.in"

for profile in profiles:
    email = generate_email(profile['name'], profile['officer_id'])
    profile['email'] = email
    
    # Create in Firebase Auth
    try:
        auth.create_user(
            email=email,
            password='123456',
            display_name=profile['name']
        )
        print(f"Created: {email}")
    except Exception as e:
        print(f"Error creating {email}: {e}")

# Save updated profiles back to JSON
with open(profiles_path, 'w') as f:
    json.dump(profiles, f, indent=2)

print("Saved updated profiles to data/official_profiles.json!")
