import http.server
import socketserver
import json
import os
import urllib.parse
import traceback

PORT = 8051
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
DATA_DIR = os.path.join(BASE_DIR, "data")
DASHBOARD_DATA_DIR = os.path.join(DASHBOARD_DIR, "data")

from competency_engine import CompetencyEngine, COMPETENCY_FRAMEWORK, CADRE_ROLE_REQUIREMENTS, DIVISIONS
from recommendation_engine import RecommendationEngine
from assessment_generator import AssessmentEngine

competency_engine = CompetencyEngine()
recommendation_engine = RecommendationEngine()
assessment_engine = AssessmentEngine()

class DebugHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        try:
            if path == "/api/igot/courses":
                courses = recommendation_engine.igot_courses
                self.send_json_response(courses)
                return

            elif path == "/api/nssta/programmes":
                self.send_json_response(recommendation_engine.tpac_programmes)
                return

            elif path == "/api/materials":
                self.send_json_response(assessment_engine.get_all_materials())
                return

            elif path == "/api/assessments":
                self.send_json_response(assessment_engine.get_all_assessments())
                return

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_data = {"error": str(e), "traceback": traceback.format_exc()}
            self.wfile.write(json.dumps(error_data).encode("utf-8"))
            return

        return super().do_GET()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), DebugHandler) as httpd:
    print(f"Debug server at http://localhost:{PORT}/")
    httpd.serve_forever()