"""
Master Pipeline Runner for SKILL-STAT (Folder 101)
AI-Enabled Skill Intelligence, Competency Gap Analysis, iGOT Karmayogi & NSSTA Integration,
and Intelligent Assessment Generation for India's Official Statistical System.

Orchestrates:
1. Official Statistical Competency Taxonomy & Officer Profiler (2,850+ Profiles)
2. Dual-Track Hybrid Recommendation Engine (iGOT Karmayogi + NSSTA TPAC)
3. AI Assessment & Generative MCQ Bank Compilation
4. Publication-Grade MoSPI Executive Flash Report Generation (PDF)
5. Starting SKILL-STAT Web Server on http://localhost:8001/
"""

import sys
import subprocess
import os
import time

def run_step(step_name, script_name):
    print(f"\n==================================================================")
    print(f"  STEP: {step_name}")
    print(f"==================================================================")
    python_exe = sys.executable
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    result = subprocess.run([python_exe, script_path], cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        print(f"[!] Step {step_name} failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main():
    print("""
  ######################################################################
  #                                                                    #
  #   SKILL-STAT: AI SKILL INTELLIGENCE & LEARNING PLATFORM            #
  #   Capacity Building for India's Official Statistical System        #
  #   MoSPI • NSSTA • Mission Karmayogi (Folder 101)                   #
  #                                                                    #
  ######################################################################
    """)

    # Step 1: Competency Engine
    run_step("1. Official Competency Profiling & Gap Analysis (2,850 Cadre Profiles)", "competency_engine.py")

    # Step 2: Hybrid Recommendation Engine
    run_step("2. Dual-Track iGOT Karmayogi & NSSTA TPAC Recommendation Engine", "recommendation_engine.py")

    # Step 3: Assessment Generator
    run_step("3. AI Generative Assessment Engine & MCQ Bank Compilation", "assessment_generator.py")

    # Step 4: Publication-Grade PDF Report
    run_step("4. Generating Publication-Grade Executive Report (PDF)", "generate_pdf_report_101.py")

    # Step 5: Launch Web Server
    print(f"\n==================================================================")
    print(f"  LAUNCHING SKILL-STAT PLATFORM WEB SERVER (Port 8050)")
    print(f"  Access the Portal at: http://localhost:8050/")
    print(f"==================================================================\n")
    import server
    server.start_server()

if __name__ == "__main__":
    main()
