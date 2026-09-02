import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

DATA_DIR = "data"
DASHBOARD_DATA_DIR = "dashboard/data"

def upload_json_to_firestore(file_path, collection_name, is_list=False, id_field=None):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    collection_ref = db.collection(collection_name)

    if is_list:
        if isinstance(data, list):
            for item in data:
                # Use a specific field as document ID if provided, else auto-generate
                doc_id = item.get(id_field) if id_field else None
                if doc_id:
                    collection_ref.document(str(doc_id)).set(item)
                else:
                    collection_ref.add(item)
            print(f"Uploaded list to '{collection_name}': {len(data)} items")
    else:
        if isinstance(data, dict):
            # If it's a dict where keys are IDs (like assessment_bank)
            for key, val in data.items():
                if isinstance(val, dict):
                    collection_ref.document(str(key)).set(val)
                else:
                    collection_ref.document("data").set(data)
                    break
            print(f"Uploaded dict to '{collection_name}'")

def main():
    print("Starting database migration to Firebase Firestore...")
    
    # 1. Official Profiles
    upload_json_to_firestore(f"{DATA_DIR}/official_profiles.json", "official_profiles", is_list=True, id_field="officer_id")
    
    # 2. Competency Framework
    # It's a dict, we can store it as a single document in a 'config' collection
    with open(f"{DATA_DIR}/competency_framework.json", 'r', encoding='utf-8') as f:
        cf_data = json.load(f)
        db.collection("config").document("competency_framework").set({"data": cf_data})
        print("Uploaded Competency Framework")

    # 3. iGOT Courses
    upload_json_to_firestore(f"{DATA_DIR}/igot_course_catalog.json", "igot_courses", is_list=True, id_field="course_id")
    
    # 4. NSSTA TPAC
    upload_json_to_firestore(f"{DATA_DIR}/nssta_tpac_catalog.json", "nssta_tpac_programmes", is_list=True, id_field="programme_id")
    
    # 5. Assessment Bank
    upload_json_to_firestore(f"{DATA_DIR}/assessment_bank.json", "assessments", is_list=False)
    
    # 6. Learning Materials
    upload_json_to_firestore(f"{DATA_DIR}/learning_materials.json", "learning_materials", is_list=False)

    # 7. Primary Learner
    primary_learner_path = f"{DASHBOARD_DATA_DIR}/primary_learner.json"
    if os.path.exists(primary_learner_path):
        with open(primary_learner_path, 'r', encoding='utf-8') as f:
            db.collection("official_profiles").document("OFF-ISS-2026-HQ").set(json.load(f))
            print("Uploaded Primary Learner profile")

    print("Migration complete!")

if __name__ == "__main__":
    main()
