import json
import random
import firebase_admin
from firebase_admin import credentials, firestore

def main():
    cred = credentials.Certificate("firebase_credentials.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    collection_ref = db.collection("official_profiles")
    docs = list(collection_ref.stream())
    
    print(f"Found {len(docs)} profiles in Firestore.")
    
    if len(docs) > 100:
        kept_docs = random.sample(docs, 100)
        kept_ids = {doc.id for doc in kept_docs}
        
        batch = db.batch()
        deleted_count = 0
        
        for doc in docs:
            if doc.id not in kept_ids:
                batch.delete(doc.reference)
                deleted_count += 1
                
                # Firestore batch has a limit of 500 operations
                if deleted_count % 400 == 0:
                    batch.commit()
                    batch = db.batch()
                    print(f"Deleted {deleted_count} so far...")
                    
        if deleted_count % 400 != 0:
            batch.commit()
            
        print(f"Deleted {deleted_count} profiles. Kept 100.")
        
        # Save the 100 profiles to local JSON
        kept_profiles = [doc.to_dict() for doc in kept_docs]
        with open("data/official_profiles.json", "w", encoding="utf-8") as f:
            json.dump(kept_profiles, f, indent=4)
        print("Updated data/official_profiles.json with 100 profiles.")
        
        # Update administrative_analytics.json
        try:
            with open("data/administrative_analytics.json", "r", encoding="utf-8") as f:
                analytics = json.load(f)
            
            analytics["total_officers"] = 100
            
            with open("data/administrative_analytics.json", "w", encoding="utf-8") as f:
                json.dump(analytics, f, indent=4)
                
            with open("dashboard/data/administrative_analytics.json", "w", encoding="utf-8") as f:
                json.dump(analytics, f, indent=4)
                
            print("Updated administrative_analytics.json to 100.")
        except Exception as e:
            print("Error updating analytics JSON:", e)
    else:
        print("There are 100 or fewer profiles. No deletion needed.")

if __name__ == "__main__":
    main()
