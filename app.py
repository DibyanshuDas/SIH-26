from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from assessment_generator import AssessmentEngine

assessment_engine = AssessmentEngine()

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
    officer_id = request.args.get('id')
    role_key = request.args.get('role')
    
    if role_key:
        docs = db.collection('official_profiles').where('role_key', '==', role_key).limit(1).stream()
        for doc in docs:
            return jsonify(doc.to_dict())
    
    if officer_id:
        doc = db.collection('official_profiles').document(officer_id).get()
        if doc.exists:
            return jsonify(doc.to_dict())
            
    # Default fallback
    doc = db.collection('official_profiles').document('OFF-ISS-2026-HQ').get()
    if doc.exists:
        return jsonify(doc.to_dict())
        
    return jsonify({"error": "Profile not found"}), 404

@app.route('/api/skill-gaps', methods=['GET'])
def get_skill_gaps():
    officer_id = request.args.get('id', 'OFF-ISS-2026-HQ')
    doc = db.collection('official_profiles').document(officer_id).get()
    if doc.exists:
        profile = doc.to_dict()
        return jsonify({
            "officer_id": profile.get("officer_id"),
            "overall_competency_index": profile.get("overall_competency_index"),
            "domain_scores": profile.get("domain_scores", {}),
            "skill_gaps": profile.get("skill_gaps", {}),
            "top_priority_gaps": profile.get("top_priority_gaps", [])
        })
    return jsonify({"error": "Profile not found"}), 404

@app.route('/api/officers', methods=['GET'])
def get_officers():
    division = request.args.get('division')
    cadre = request.args.get('cadre')
    page = int(request.args.get('page', 1))
    
    query = db.collection('official_profiles')
    if division and division != "All":
        query = query.where('division_code', '==', division)
    if cadre and cadre != "All":
        query = query.where('cadre', '==', cadre)
        
    docs = query.order_by('officer_id').offset((page - 1) * 15).limit(15).stream()
    return jsonify([d.to_dict() for d in docs])

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    officer_id = request.args.get('id', 'OFF-ISS-2026-HQ')
    officer_doc = db.collection('official_profiles').document(officer_id).get()
    
    if not officer_doc.exists:
        return jsonify({"error": "Profile not found"}), 404
        
    officer = officer_doc.to_dict()
    current_index = officer.get("overall_competency_index", 70.0)
    
    # Fetch from igot_courses and nssta_tpac_programmes
    courses = [doc.to_dict() for doc in db.collection('igot_courses').stream()]
    tpac = [doc.to_dict() for doc in db.collection('nssta_tpac_programmes').stream()]
    
    # Inject mock uplift for UI if missing
    for c in courses:
        if "estimated_uplift_pct" not in c:
            c["estimated_uplift_pct"] = round(4.5 + (hash(c.get("course_id", "")) % 30) / 10.0, 1)

    return jsonify({
      "officer_id": officer_id,
      "officer_name": officer.get("name", "Officer"),
      "current_competency_index": current_index,
      "projected_competency_index": round(current_index + 16.2, 1),
      "potential_gain_pct": 16.2,
      "learning_pathway": {
        "stage_1_urgent_gap_closure": courses[:3],
        "stage_2_applied_modernization": courses[3:6] if len(courses) > 5 else courses[:2],
        "stage_3_leadership_strategic": courses[6:8] if len(courses) > 7 else courses[:1]
      },
      "nssta_executive_programmes": tpac[:2]
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
    materials_file = os.path.join(os.path.dirname(__file__), "data", "learning_materials.json")
    if os.path.exists(materials_file):
        with open(materials_file, "r") as f:
            materials = json.load(f)
            # Re-key them by id for the frontend
            return jsonify({m.get('id', str(i)): m for i, m in enumerate(materials)})
    return jsonify({})

@app.route('/api/assessments', methods=['GET'])
def get_assessments():
    assessments_file = os.path.join(os.path.dirname(__file__), "data", "assessment_bank.json")
    if os.path.exists(assessments_file):
        with open(assessments_file, "r") as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/assessments/generate', methods=['POST'])
def generate_assessment():
    payload = request.json or {}
    title = payload.get("title", "Uploaded Statistical Guidelines")
    content = payload.get("content", "")
    target_comp = payload.get("target_competency", "STAT-01")
    num_q = int(payload.get("num_questions", 5))

    if not content.strip():
        # Pick from default material if empty
        mats = list(assessment_engine.materials.values())
        content = mats[0]["content"]
        title = mats[0]["title"]

    generated_asm = assessment_engine.generate_assessment_from_text(title, content, target_comp, num_q)
    return jsonify(generated_asm)

@app.route('/api/assessments/submit', methods=['POST'])
def submit_assessment():
    payload = request.json or {}
    officer_id = payload.get("officer_id", "OFF-ISS-2026-HQ")
    asm_id = payload.get("assessment_id")
    answers = payload.get("answers", {})

    result = assessment_engine.grade_submission(officer_id, asm_id, answers)
    
    # Update karma points in Firebase as well
    officer_ref = db.collection('official_profiles').document(officer_id)
    officer_doc = officer_ref.get()
    if officer_doc.exists:
        officer = officer_doc.to_dict()
        officer['karma_points'] = officer.get('karma_points', 0) + result.get('karma_points_earned', 0)
        officer_ref.set(officer)

    return jsonify(result)

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


@app.route('/api/admin/analytics', methods=['GET'])
def get_admin_analytics():
    # Read the analytics from local data file, because it wasn't migrated to Firestore
    analytics_file = os.path.join(os.path.dirname(__file__), "data", "administrative_analytics.json")
    if os.path.exists(analytics_file):
        with open(analytics_file, "r") as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/assistant/query', methods=['POST'])
def assistant_query():
    payload = request.json or {}
    query = payload.get("query", "")
    officer_id = payload.get("officer_id", "OFF-ISS-2026-HQ")
    
    q_lower = query.lower()
    
    if "gap" in q_lower or "skill" in q_lower or "deficiencies" in q_lower:
        response = {
            "answer": "Based on your competency profile, your top priority skill gap is in **Modern Python for Microdata Processing (TECH-01)** (Gap: -2 Levels) and **AI & Machine Learning for Survey Nowcasting (TECH-07)**. Closing these gaps will elevate your Competency Readiness Index from **78.4% to 86.8%**.",
            "suggested_actions": ["Enrol in 'Python for Official Statistics (IGOT-TECH-201)'", "Take the Python Microdata Assessment", "Register for NSSTA-TPAC AI Workshop"],
            "recommended_course_id": "IGOT-TECH-201"
        }
    elif "national account" in q_lower or "sna" in q_lower or "gdp" in q_lower:
        response = {
            "answer": "Under **SNA 2008** standards, Gross Value Added (GVA) at basic prices is defined as Gross Output minus Intermediate Consumption. GDP at market prices is derived by adding Net Product Taxes (Product Taxes - Product Subsidies). Supply-Use Tables (SUT) serve as the fundamental diagnostic tool for sector balancing.",
            "suggested_actions": ["Take the National Accounts Assessment", "Enrol in 'System of National Accounts & GDP (IGOT-STAT-102)'", "View SUT Module Syllabus"],
            "recommended_course_id": "IGOT-STAT-102"
        }
    elif "cpi" in q_lower or "price" in q_lower or "inflation" in q_lower:
        response = {
            "answer": "The All-India CPI utilizes a **Modified Laspeyres price index** formula with base expenditure weights from the Household Consumption Expenditure Survey (HCES). At elementary aggregate levels, MoSPI mandates the **Jevons Index (geometric mean)** because it avoids the upward bias of Carli and satisfies the axiomatic time-reversal test.",
            "suggested_actions": ["Take CPI Compilation Quiz", "Explore 'Consumer Price Index & Inflation (IGOT-STAT-103)'"],
            "recommended_course_id": "IGOT-STAT-103"
        }
    elif "plfs" in q_lower or "labour" in q_lower or "employment" in q_lower:
        response = {
            "answer": "The **Periodic Labour Force Survey (PLFS)** measures employment under two main criteria: **Usual Status (UPSS)** (major time >= 183 days + subsidiary work >= 30 days) and **Current Weekly Status (CWS)** (at least 1 hour of work on any 1 day during 7-day recall). In urban areas, a 25% rotational panel across 4 consecutive quarters is deployed.",
            "suggested_actions": ["Take PLFS Standards Quiz", "Enrol in 'PLFS Concepts & Data Analytics (IGOT-STAT-105)'"],
            "recommended_course_id": "IGOT-STAT-105"
        }
    elif "dpdpa" in q_lower or "privacy" in q_lower or "confidentiality" in q_lower:
        response = {
            "answer": "Under the **Digital Personal Data Protection Act 2023 (DPDPA)**, MoSPI operates as a Significant Data Fiduciary. Before releasing public microdata, Statistical Disclosure Control (SDC) requires eliminating direct identifiers, enforcing **k-Anonymity (k >= 5)** on quasi-identifiers, and top-coding high-income outliers to prevent re-identification.",
            "suggested_actions": ["Take DPDPA 2023 Compliance Quiz", "Enrol in 'DPDPA 2023 & Microdata Privacy (IGOT-GOV-302)'"],
            "recommended_course_id": "IGOT-GOV-302"
        }
    else:
        response = {
            "answer": f"I am your **KASHYAP AI Karmayogi Statistical Learning Assistant**. I can help you analyze your competency gaps, recommend iGOT Karmayogi micro-courses, navigate NSSTA TPAC in-service workshops, and explain statistical methodologies across SNA 2008, CPI, PLFS, Python for microdata, and DPDPA 2023.",
            "suggested_actions": ["Analyze my skill gaps", "Recommend iGOT courses for my role", "Generate an AI MCQ Quiz from a circular"],
            "recommended_course_id": "IGOT-STAT-101"
        }
        
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port)
