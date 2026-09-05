import json
import firebase_admin
from firebase_admin import credentials, firestore

def sync_profiles():
    cred = credentials.Certificate("firebase_credentials.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    with open("data/official_profiles.json", "r", encoding="utf-8") as f:
        profiles = json.load(f)
        
    print(f"Loaded {len(profiles)} profiles from data/official_profiles.json")
    
    batch = db.batch()
    count = 0
    for profile in profiles:
        doc_ref = db.collection("official_profiles").document(profile["officer_id"])
        # merge=True preserves any existing enrolled/completed courses while updating email etc.
        batch.set(doc_ref, profile, merge=True)
        count += 1
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            
    batch.commit()
    print(f"Successfully synced {count} profiles to Firestore!")

if __name__ == "__main__":
    sync_profiles()
