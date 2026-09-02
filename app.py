from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__, static_folder='dashboard')
CORS(app)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase_credentials.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def serve_dashboard():
    return send_from_directory('dashboard', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('dashboard', path)

@app.route('/api/framework', methods=['GET'])
def get_framework():
    doc = db.collection('config').document('competency_framework').get()
    return jsonify(doc.to_dict().get('data', {}) if doc.exists else {})

@app.route('/api/learner-profile', methods=['GET'])
def get_learner_profile():
    officer_id = request.args.get('id', 'OFF-ISS-2026-HQ')
    doc = db.collection('official_profiles').document(officer_id).get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Profile not found"}), 404

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    # Fetch from igot_courses and nssta_tpac_programmes
    courses = [doc.to_dict() for doc in db.collection('igot_courses').stream()]
    tpac = [doc.to_dict() for doc in db.collection('nssta_tpac_programmes').stream()]
    
    # Return simple logic or just all for now
    return jsonify({
        "igot_courses": courses[:3],
        "nssta_tpac": tpac[:1]
    })

@app.route('/api/igot/courses', methods=['GET'])
def get_igot_courses():
    courses = [doc.to_dict() for doc in db.collection('igot_courses').stream()]
    return jsonify(courses)

@app.route('/api/nssta/programmes', methods=['GET'])
def get_nssta_programmes():
    programmes = [doc.to_dict() for doc in db.collection('nssta_tpac_programmes').stream()]
    return jsonify(programmes)

@app.route('/api/materials', methods=['GET'])
def get_materials():
    materials = [doc.to_dict() for doc in db.collection('learning_materials').stream()]
    return jsonify({m.get('id', str(i)): m for i, m in enumerate(materials)})

@app.route('/api/assessments', methods=['GET'])
def get_assessments():
    assessments = [doc.to_dict() for doc in db.collection('assessments').stream()]
    return jsonify({a.get('assessment_id', str(i)): a for i, a in enumerate(assessments)})

@app.route('/api/igot/enrol', methods=['POST'])
def enrol_course():
    data = request.json
    course_id = data.get('course_id')
    officer_id = data.get('officer_id', 'OFF-ISS-2026-HQ')
    
    officer_ref = db.collection('official_profiles').document(officer_id)
    officer_doc = officer_ref.get()
    if not officer_doc.exists:
        return jsonify({"error": "Profile not found"}), 404
        
    officer = officer_doc.to_dict()
    # Simple simulated uplift logic
    officer['karma_points'] = officer.get('karma_points', 0) + 50
    officer['total_learning_hours'] = officer.get('total_learning_hours', 0) + 2
    officer_ref.set(officer)
    
    return jsonify({
        "success": True,
        "message": f"Successfully enrolled & completed certification!",
        "new_competency_index": officer.get('overall_competency_index', 0),
        "karma_points_earned": 50,
        "updated_officer": officer
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port)
