import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

courses = [doc.to_dict() for doc in db.collection('igot_courses').stream()]
print(f"Loaded {len(courses)} courses.")
