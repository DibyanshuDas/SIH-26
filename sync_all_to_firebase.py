import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def sync_all_data():
    cred_path = "firebase_credentials.json"
    if not os.path.exists(cred_path):
        print("firebase_credentials.json not found!")
        return

    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    dashboard_data_dir = os.path.join(base_dir, "dashboard", "data")

    # 1. Sync official_profiles
    profiles_path = os.path.join(data_dir, "official_profiles.json")
    if os.path.exists(profiles_path):
        with open(profiles_path, "r", encoding="utf-8") as f:
            profiles = json.load(f)
        print(f"Syncing {len(profiles)} profiles to 'official_profiles'...")
        batch = db.batch()
        count = 0
        for p in profiles:
            doc_ref = db.collection("official_profiles").document(p["officer_id"])
            batch.set(doc_ref, p, merge=True)
            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()
        batch.commit()
        print(f"-> Successfully synced {count} official profiles!")

    # 2. Sync igot_course_catalog
    igot_path = os.path.join(data_dir, "igot_course_catalog.json")
    if os.path.exists(igot_path):
        with open(igot_path, "r", encoding="utf-8") as f:
            courses = json.load(f)
        print(f"Syncing {len(courses)} courses to 'igot_courses'...")
        batch = db.batch()
        for c in courses:
            doc_ref = db.collection("igot_courses").document(c["course_id"])
            batch.set(doc_ref, c, merge=True)
        batch.commit()
        print(f"-> Successfully synced {len(courses)} iGOT courses!")

    # 3. Sync nssta_tpac_catalog
    nssta_path = os.path.join(data_dir, "nssta_tpac_catalog.json")
    if os.path.exists(nssta_path):
        with open(nssta_path, "r", encoding="utf-8") as f:
            programmes = json.load(f)
        print(f"Syncing {len(programmes)} programmes to 'nssta_tpac_programmes'...")
        batch = db.batch()
        for prog in programmes:
            doc_ref = db.collection("nssta_tpac_programmes").document(prog["program_id"])
            batch.set(doc_ref, prog, merge=True)
        batch.commit()
        print(f"-> Successfully synced {len(programmes)} NSSTA programmes!")

    # 4. Sync assessment_bank
    assessment_path = os.path.join(data_dir, "assessment_bank.json")
    if os.path.exists(assessment_path):
        with open(assessment_path, "r", encoding="utf-8") as f:
            assessments = json.load(f)
        print(f"Syncing {len(assessments)} assessments to 'assessment_bank'...")
        batch = db.batch()
        for asm in assessments:
            doc_ref = db.collection("assessment_bank").document(asm.get("assessment_id", asm.get("material_id")))
            batch.set(doc_ref, asm, merge=True)
        batch.commit()
        print(f"-> Successfully synced {len(assessments)} assessments!")

    # 5. Sync learning_materials
    materials_path = os.path.join(data_dir, "learning_materials.json")
    if os.path.exists(materials_path):
        with open(materials_path, "r", encoding="utf-8") as f:
            materials_data = json.load(f)
        if isinstance(materials_data, dict):
            materials_list = list(materials_data.values())
        else:
            materials_list = materials_data
        print(f"Syncing {len(materials_list)} learning materials to 'learning_materials'...")
        batch = db.batch()
        for mat in materials_list:
            doc_ref = db.collection("learning_materials").document(mat["id"])
            batch.set(doc_ref, mat, merge=True)
        batch.commit()
        print(f"-> Successfully synced {len(materials_list)} learning materials!")

    # 6. Sync administrative_analytics into config
    analytics_path = os.path.join(data_dir, "administrative_analytics.json")
    if os.path.exists(analytics_path):
        with open(analytics_path, "r", encoding="utf-8") as f:
            analytics = json.load(f)
        db.collection("config").document("administrative_analytics").set({"data": analytics}, merge=True)
        print("-> Successfully synced 'administrative_analytics' to config collection!")

    # 7. Sync competency_framework into config
    fw_path = os.path.join(data_dir, "competency_framework.json")
    if os.path.exists(fw_path):
        with open(fw_path, "r", encoding="utf-8") as f:
            fw = json.load(f)
        db.collection("config").document("competency_framework").set({"data": fw}, merge=True)
        print("-> Successfully synced 'competency_framework' to config collection!")

    # 8. Sync leaderboard
    lb_path = os.path.join(dashboard_data_dir, "leaderboard.json")
    if os.path.exists(lb_path):
        with open(lb_path, "r", encoding="utf-8") as f:
            leaderboard = json.load(f)
        db.collection("config").document("leaderboard").set({"data": leaderboard}, merge=True)
        print("-> Successfully synced 'leaderboard' to config collection!")

    # 9. Sync primary_recommendations
    rec_path = os.path.join(data_dir, "primary_recommendations.json")
    if os.path.exists(rec_path):
        with open(rec_path, "r", encoding="utf-8") as f:
            recs = json.load(f)
        db.collection("config").document("primary_recommendations").set({"data": recs}, merge=True)
        db.collection("recommendations").document("OFF-ISS-2026-HQ").set(recs, merge=True)
        print("-> Successfully synced 'primary_recommendations' to config and recommendations collection!")

    # 10. Sync primary_learner
    learner_path = os.path.join(dashboard_data_dir, "primary_learner.json")
    if os.path.exists(learner_path):
        with open(learner_path, "r", encoding="utf-8") as f:
            learner = json.load(f)
        db.collection("official_profiles").document(learner.get("officer_id", "OFF-ISS-2026-HQ")).set(learner, merge=True)
        print("-> Successfully synced 'primary_learner' to official_profiles document!")

    print("\nALL DATA SUCCESSFULLY SYNCHRONIZED TO FIREBASE FIRESTORE!")

if __name__ == "__main__":
    sync_all_data()
