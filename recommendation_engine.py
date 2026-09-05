"""
Hybrid AI Recommendation Engine for India's Official Statistical System
Integrates with:
- iGOT Karmayogi Digital Micro-Course Ecosystem
- NSSTA (National Statistical Systems Training Academy) TPAC Annual Training Programme
Provides Semantic Match, Gap Closure Prioritization & Career Pathway Navigation.
"""

import json
import os
from typing import Dict, List, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DASHBOARD_DATA_DIR = os.path.join(BASE_DIR, "dashboard", "data")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DATA_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. iGOT Karmayogi Official Course Catalog (Curated for Official Statistics)
# -------------------------------------------------------------------------
IGOT_COURSES = [
    {
        "course_id": "IGOT-STAT-101",
        "title": "Modern Survey Sampling & Complex Multi-Stage Design",
        "provider": "NSSTA & Indian Statistical Institute (ISI)",
        "duration_hours": 12,
        "level": "Intermediate",
        "primary_competency": "STAT-01",
        "competency_tags": ["STAT-01", "STAT-08", "TECH-02"],
        "rating": 4.9,
        "enrolled_count": 1420,
        "description": "Master probability proportional to size (PPS) sampling, stratified cluster design, variance estimation, and non-response calibration in large-scale national surveys.",
        "syllabus": [
            "Module 1: Foundations of Probability Sampling vs Purposive Frames",
            "Module 2: Multi-Stage Stratified Sampling in NSS Rounds",
            "Module 3: Sub-Sample Replicate Variance Estimation (Jackknife & Bootstrap)",
            "Module 4: Multiplier and Multi-Stage Weight Calculation"
        ],
        "badge_name": "Certified Survey Sampling Specialist",
        "karma_points": 180
    },
    {
        "course_id": "IGOT-STAT-102",
        "title": "System of National Accounts (SNA 2008) & GDP Compilation",
        "provider": "National Accounts Division (NAD) & IMF",
        "duration_hours": 16,
        "level": "Advanced",
        "primary_competency": "STAT-02",
        "competency_tags": ["STAT-02", "STAT-08", "LEAD-01"],
        "rating": 4.95,
        "enrolled_count": 980,
        "description": "Comprehensive practical deep-dive into Gross Value Added (GVA) at basic prices, Supply-Use Tables (SUT), Sequence of Accounts, and FISIM allocation.",
        "syllabus": [
            "Module 1: Production Boundary and Institutional Sector Classifications",
            "Module 2: GVA Estimation across Agriculture, Industry and Services",
            "Module 3: Supply-Use Tables (SUT) Balancing & Input-Output Matrices",
            "Module 4: Financial Accounts, Balance Sheets & Capital Stock Estimation"
        ],
        "badge_name": "National Accounts Master Practitioner",
        "karma_points": 240
    },
    {
        "course_id": "IGOT-STAT-103",
        "title": "Consumer Price Index (CPI) & Inflation Measurement Methodologies",
        "provider": "Economic Statistics Division (ESD) & MoSPI",
        "duration_hours": 8,
        "level": "Intermediate",
        "primary_competency": "STAT-03",
        "competency_tags": ["STAT-03", "STAT-08", "TECH-01"],
        "rating": 4.8,
        "enrolled_count": 1640,
        "description": "Practical workflows for price collection, geometric mean vs ratio of arithmetic means, chain-linking, core inflation derivation, and housing index imputation.",
        "syllabus": [
            "Module 1: CPI Urban/Rural/Combined Architecture and Laspeyres Index",
            "Module 2: Price Quotation Scrutiny & Missing Price Imputation",
            "Module 3: Geometric Mean Jevons Price Indices at Item Level",
            "Module 4: Base Year Revision & Item Basket Recalibration Protocols"
        ],
        "badge_name": "Price Index Analyst",
        "karma_points": 120
    },
    {
        "course_id": "IGOT-STAT-104",
        "title": "Annual Survey of Industries (ASI) & IIP Index Compilation",
        "provider": "Economic Statistics Division (ESD)",
        "duration_hours": 10,
        "level": "Intermediate",
        "primary_competency": "STAT-04",
        "competency_tags": ["STAT-04", "TECH-03", "STAT-08"],
        "rating": 4.75,
        "enrolled_count": 1120,
        "description": "Understand factory sector frame validation, Block-wise scrutiny in ASI schedules, GVA in manufacturing, and monthly IIP production index tracking.",
        "syllabus": [
            "Module 1: ASI Census vs Sample Sectors and Frame Updating",
            "Module 2: Scrutiny of Capital, Inputs, Outputs, and Depreciation Blocks",
            "Module 3: Index of Industrial Production (IIP) Item Weighting and Production Growth",
            "Module 4: Reconciling ASI with MCA-21 Corporate Registry Data"
        ],
        "badge_name": "Industrial Statistics Specialist",
        "karma_points": 150
    },
    {
        "course_id": "IGOT-STAT-105",
        "title": "Periodic Labour Force Survey (PLFS) Concepts & Data Analytics",
        "provider": "Social Statistics Division (SSD) & ILO",
        "duration_hours": 10,
        "level": "Intermediate",
        "primary_competency": "STAT-05",
        "competency_tags": ["STAT-05", "TECH-01", "STAT-07"],
        "rating": 4.9,
        "enrolled_count": 1890,
        "description": "Master activity status classifications (ps+ss, cws), hours worked, informal enterprise employment, earnings distribution, and quarterly urban bulletin analytics.",
        "syllabus": [
            "Module 1: Usual Status vs Current Weekly Status Activity Frameworks",
            "Module 2: Labour Force Participation Rate (LFPR) and Unemployment Rates",
            "Module 3: Rotational Panel Sampling in Urban PLFS",
            "Module 4: Analyzing Microdata in Python and R for Policy Reports"
        ],
        "badge_name": "Labour Statistics Expert",
        "karma_points": 150
    },
    {
        "course_id": "IGOT-STAT-107",
        "title": "SDG National Indicator Framework (NIF) Monitoring & Data Disaggregation",
        "provider": "MoSPI SDG Unit & NITI Aayog",
        "duration_hours": 8,
        "level": "Foundation",
        "primary_competency": "STAT-07",
        "competency_tags": ["STAT-07", "STAT-09", "LEAD-01"],
        "rating": 4.85,
        "enrolled_count": 2100,
        "description": "Aligning national datasets with 17 UN SDGs, MoSPI NIF 3.0 metadata protocols, state/district SDG localization, and vulnerability disaggregation.",
        "syllabus": [
            "Module 1: 2030 Agenda & India's National Indicator Framework (NIF)",
            "Module 2: Standardizing Indicator Definitions & Tier Classifications",
            "Module 3: Multi-Source Harmonization (Surveys, Administrative Registries)",
            "Module 4: MoSPI SDG Dashboard Publishing and Policy Feedback"
        ],
        "badge_name": "SDG Statistical Practitioner",
        "karma_points": 120
    },
    {
        "course_id": "IGOT-STAT-108",
        "title": "National Quality Assurance Framework (NQAF) & Audit Protocols",
        "provider": "NSSTA & UN Statistics Division",
        "duration_hours": 6,
        "level": "Intermediate",
        "primary_competency": "STAT-08",
        "competency_tags": ["STAT-08", "STAT-10", "LEAD-04"],
        "rating": 4.9,
        "enrolled_count": 870,
        "description": "Applying UN-NQAF across survey lifecycle: managing statistical processes, error prevention, metadata transparency, and peer review audits.",
        "syllabus": [
            "Module 1: Principles of UN-NQAF and MoSPI Quality Policy",
            "Module 2: Managing Process Quality from Design to Dissemination",
            "Module 3: Quality Reporting & Producer-User Dialogue",
            "Module 4: Institutional Audits of Official Statistical Releases"
        ],
        "badge_name": "Quality Assurance Auditor",
        "karma_points": 90
    },
    {
        "course_id": "IGOT-TECH-201",
        "title": "Python for Official Statistics: Microdata Wrangling & Analysis",
        "provider": "Data Informatics & Innovation Division (DIID) & IIT Madras",
        "duration_hours": 20,
        "level": "Intermediate",
        "primary_competency": "TECH-01",
        "competency_tags": ["TECH-01", "TECH-03", "TECH-06"],
        "rating": 4.95,
        "enrolled_count": 3120,
        "description": "Modern Python workflow for official statisticians: reading fixed-width NSS microdata, Pandas/Polars aggregation, automated tabulations, and statistical tests.",
        "syllabus": [
            "Module 1: Fast I/O with Large Government Datasets (Parquet, Polars)",
            "Module 2: Microdata Cleaning, Anomaly Identification & Imputation",
            "Module 3: Automated Survey Multiplier Application & Tabulation",
            "Module 4: Scripting Automated Monthly Statistical Bulletins"
        ],
        "badge_name": "Statistical Python Developer",
        "karma_points": 300
    },
    {
        "course_id": "IGOT-TECH-202",
        "title": "Advanced Survey Data Modeling & Econometrics in R",
        "provider": "NSSTA & Delhi School of Economics",
        "duration_hours": 18,
        "level": "Advanced",
        "primary_competency": "TECH-02",
        "competency_tags": ["TECH-02", "STAT-01", "TECH-07"],
        "rating": 4.88,
        "enrolled_count": 1780,
        "description": "Using R's survey, srvyr, and surveyplanning packages for complex sampling variance estimation, Small Area Estimation (SAE), and econometric causal inference.",
        "syllabus": [
            "Module 1: Declaring Survey Designs (`svydesign`) and Replicate Weights",
            "Module 2: Generalized Linear Models with Complex Survey Weights",
            "Module 3: Small Area Estimation (Fay-Herriot & Unit-Level EBLUP)",
            "Module 4: R Markdown for Reproducible Official Statistical Publications"
        ],
        "badge_name": "R Survey Modeling Specialist",
        "karma_points": 270
    },
    {
        "course_id": "IGOT-TECH-203",
        "title": "SQL Data Pipelines & Statistical Warehousing on MeghRaj Cloud",
        "provider": "NIC & MoSPI IT Division",
        "duration_hours": 14,
        "level": "Intermediate",
        "primary_competency": "TECH-03",
        "competency_tags": ["TECH-03", "TECH-08", "GOV-01"],
        "rating": 4.78,
        "enrolled_count": 1450,
        "description": "Master SQL window functions, distributed query execution, census table indexing, and ETL pipelines for administrative data ingestion into MoSPI Data Lake.",
        "syllabus": [
            "Module 1: Advanced SQL Joins, CTEs, and Window Aggregations",
            "Module 2: Relational Schema vs Columnar Stores (ClickHouse/DuckDB)",
            "Module 3: Automated Quality Validation Checks in ETL Pipelines",
            "Module 4: REST API Integration with Government Portals"
        ],
        "badge_name": "Data Pipeline Architect",
        "karma_points": 210
    },
    {
        "course_id": "IGOT-TECH-205",
        "title": "Geospatial Statistics & GIS Integration (Bhuvan, QGIS & Spatial R)",
        "provider": "ISRO & National Remote Sensing Centre (NRSC)",
        "duration_hours": 15,
        "level": "Intermediate",
        "primary_competency": "TECH-05",
        "competency_tags": ["TECH-05", "STAT-06", "STAT-01"],
        "rating": 4.92,
        "enrolled_count": 1620,
        "description": "Harness satellite imagery and spatial GIS layers for sampling frame stratification, PSU delineation, crop yield estimation, and spatial autocorrelation mapping.",
        "syllabus": [
            "Module 1: Coordinate Reference Systems & Vector/Raster Data in QGIS",
            "Module 2: Primary Sampling Unit (PSU) Digitization & Bhuvan Geo-Portal",
            "Module 3: Spatial Autocorrelation (Moran's I) & Geographically Weighted Regression",
            "Module 4: High-Resolution Crop Area Estimation via Remote Sensing"
        ],
        "badge_name": "Geospatial Statistical Analyst",
        "karma_points": 225
    },
    {
        "course_id": "IGOT-TECH-207",
        "title": "AI & Machine Learning for Nowcasting & Automated Survey Scrutiny",
        "provider": "MeitY AI Mission & NSSTA",
        "duration_hours": 16,
        "level": "Advanced",
        "primary_competency": "TECH-07",
        "competency_tags": ["TECH-07", "TECH-01", "STAT-02"],
        "rating": 4.96,
        "enrolled_count": 2240,
        "description": "Implement Random Forests, XGBoost, and Transformer LLMs for economic nowcasting, automatic classification of NIC/NCO occupation codes, and outlier detection.",
        "syllabus": [
            "Module 1: High-Frequency Economic Nowcasting with ML Algorithms",
            "Module 2: NLP for Automated Industry (NIC) & Occupation (NCO) Text Coding",
            "Module 3: Unsupervised Outlier & Anomaly Detection in CAPI Submissions",
            "Module 4: Synthetic Microdata Generation with Differential Privacy"
        ],
        "badge_name": "AI Official Statistics Specialist",
        "karma_points": 240
    },
    {
        "course_id": "IGOT-GOV-301",
        "title": "Cybersecurity & CERT-In Guidelines for Statistical Enclaves",
        "provider": "CERT-In & DoPT",
        "duration_hours": 6,
        "level": "Foundation",
        "primary_competency": "GOV-01",
        "competency_tags": ["GOV-01", "GOV-03", "TECH-08"],
        "rating": 4.82,
        "enrolled_count": 3400,
        "description": "Essential cyber hygiene, protecting statistical servers, password policies, encrypted data transfers, and compliance with national cybersecurity directives.",
        "syllabus": [
            "Module 1: Cyber Threat Landscape for Critical Government Information Systems",
            "Module 2: Enclave Isolation & Unidirectional Data Flow Architectures",
            "Module 3: CERT-In Mandatory Security Auditing & Incident Reporting",
            "Module 4: Secure Data Storage and Cryptographic Protocols"
        ],
        "badge_name": "Certified Cyber Aware Official",
        "karma_points": 90
    },
    {
        "course_id": "IGOT-GOV-302",
        "title": "Digital Personal Data Protection Act (DPDPA 2023) & Microdata Privacy",
        "provider": "Ministry of Law & Justice & MoSPI",
        "duration_hours": 8,
        "level": "Intermediate",
        "primary_competency": "GOV-02",
        "competency_tags": ["GOV-02", "STAT-10", "STAT-09"],
        "rating": 4.94,
        "enrolled_count": 2890,
        "description": "Legal obligations under DPDPA 2023 for statistical data fiduciaries: purpose limitation, consent frameworks, anonymization vs pseudonymization, and penalties.",
        "syllabus": [
            "Module 1: DPDPA 2023 Key Provisions for Government Data Collectors",
            "Module 2: Statistical Anonymization Standards (k-anonymity, l-diversity, t-closeness)",
            "Module 3: Handling Household and Enterprise Identifiable Information (PII)",
            "Module 4: Microdata Dissemination Risk Assessment Framework"
        ],
        "badge_name": "Data Privacy & Governance Officer",
        "karma_points": 120
    },
    {
        "course_id": "IGOT-LEAD-401",
        "title": "Evidence-Based Policy Formulation & Executive Statistical Advisory",
        "provider": "NITI Aayog, NSSTA & ISB Hyderabad",
        "duration_hours": 12,
        "level": "Executive",
        "primary_competency": "LEAD-01",
        "competency_tags": ["LEAD-01", "LEAD-03", "STAT-02"],
        "rating": 4.97,
        "enrolled_count": 810,
        "description": "Translating econometric and survey results into clear, actionable Cabinet notes, policy briefings, and high-impact Parliamentary committee presentations.",
        "syllabus": [
            "Module 1: Framing Macroeconomic Narratives for Decision Makers",
            "Module 2: Synthesizing Disparate Statistical Sources into Unified Briefs",
            "Module 3: Communicating Uncertainty, Margin of Error and Confidence Bounds",
            "Module 4: Case Studies: PLFS and CPI Advisory during Economic Shifts"
        ],
        "badge_name": "Strategic Statistical Policy Advisor",
        "karma_points": 180
    },
    {
        "course_id": "IGOT-LEAD-402",
        "title": "Field Survey Leadership, CAPI Operations & Logistics Management",
        "provider": "Field Operations Division (FOD) & NSSTA",
        "duration_hours": 10,
        "level": "Intermediate",
        "primary_competency": "LEAD-02",
        "competency_tags": ["LEAD-02", "STAT-01", "GOV-05"],
        "rating": 4.86,
        "enrolled_count": 1950,
        "description": "Operational mastery of field survey deployment: CAPI tablet device management, enumerator motivation, surprise inspection protocols, and community engagement.",
        "syllabus": [
            "Module 1: Nationwide Survey Round Deployment Planning & Timelines",
            "Module 2: Computer Assisted Personal Interviewing (CAPI) Supervision",
            "Module 3: Real-Time Field Verification & Re-Interviewing Protocols",
            "Module 4: Conflict Resolution and Non-Response Reduction in Urban Areas"
        ],
        "badge_name": "Survey Operations Commander",
        "karma_points": 150
    }
]

# -------------------------------------------------------------------------
# 2. NSSTA TPAC In-Service Recommended Training Programmes (Flagship)
# -------------------------------------------------------------------------
NSSTA_TPAC_PROGRAMMES = [
    {
        "program_id": "NSSTA-TPAC-2026-01",
        "title": "Advanced Residential Workshop on National Accounts & SNA Modernization",
        "format": "5-Day Full-Time Residential",
        "venue": "NSSTA Greater Noida Campus",
        "target_cadres": ["ISS (SAG, JAG, STS)", "State DES Directors"],
        "primary_competencies": ["STAT-02", "STAT-08", "TECH-01"],
        "calendar_dates": "April 14 - 18, 2026",
        "capacity_seats": 35,
        "description": "Intensive hands-on computational lab focused on compilation of Supply-Use Tables, Capital Stock, and Hedonic Quality Adjustments for the upcoming 2026-27 National Accounts Base Revision.",
        "nomination_deadline": "March 25, 2026",
        "prerequisites": "Completion of iGOT-STAT-102 or minimum 3 years experience in economic statistics."
    },
    {
        "program_id": "NSSTA-TPAC-2026-02",
        "title": "Executive Immersion in AI, Machine Learning & Big Data for Official Statistics",
        "format": "2-Week Hybrid (1 Week Virtual + 1 Week IIT Delhi Lab)",
        "venue": "IIT Delhi & NSSTA Greater Noida",
        "target_cadres": ["ISS (JAG, STS, JTS)", "DIID Technical Officers"],
        "primary_competencies": ["TECH-07", "TECH-01", "TECH-05"],
        "calendar_dates": "May 11 - 22, 2026",
        "capacity_seats": 40,
        "description": "Collaborative masterclass on implementing high-frequency economic nowcasting, transformer-based occupation code mapping, and satellite geospatial remote sensing.",
        "nomination_deadline": "April 20, 2026",
        "prerequisites": "Working knowledge of Python (Pandas/NumPy) or completion of iGOT-TECH-201."
    },
    {
        "program_id": "NSSTA-TPAC-2026-03",
        "title": "CAPI Field Operations & Quality Assurance for SSS Senior Officers",
        "format": "4-Day Regional Residential Workshop",
        "venue": "NSSTA Regional Centre (Hyderabad / Kolkata / Mumbai)",
        "target_cadres": ["SSS (SSO, JSO)", "FOD Field Superintendents"],
        "primary_competencies": ["STAT-01", "LEAD-02", "STAT-08"],
        "calendar_dates": "June 08 - 11, 2026",
        "capacity_seats": 50,
        "description": "Practical field-level troubleshooting: automated scrutiny rules, handling resistant households, GPS-tagged survey verification, and live survey administration.",
        "nomination_deadline": "May 15, 2026",
        "prerequisites": "Field posting in FOD or State Statistical Bureau."
    },
    {
        "program_id": "NSSTA-TPAC-2026-04",
        "title": "Geospatial Statistics & Frame Modernization using ISRO Bhuvan",
        "format": "5-Day Residential Workshop",
        "venue": "NRSC Hyderabad & NSSTA Greater Noida",
        "target_cadres": ["ISS (STS, JTS)", "State DES Geographers"],
        "primary_competencies": ["TECH-05", "STAT-06", "STAT-01"],
        "calendar_dates": "July 13 - 17, 2026",
        "capacity_seats": 30,
        "description": "Direct satellite GIS integration: spatial sampling frame construction, primary sampling unit (PSU) boundaries, urban slum delineation, and disaster impact assessment.",
        "nomination_deadline": "June 20, 2026",
        "prerequisites": "Completion of iGOT-TECH-205 or prior QGIS experience."
    },
    {
        "program_id": "NSSTA-TPAC-2026-05",
        "title": "Statistical Leadership, Policy Dissemination & Parliamentary Advisory",
        "format": "3-Day Executive Retreat",
        "venue": "Indian Institute of Public Administration (IIPA) New Delhi",
        "target_cadres": ["ISS (SAG, JAG)", "MoSPI Senior Management"],
        "primary_competencies": ["LEAD-01", "LEAD-03", "LEAD-05"],
        "calendar_dates": "August 04 - 06, 2026",
        "capacity_seats": 25,
        "description": "Advanced media management, proactive statistical defense, parliamentary question framing, and inter-ministerial consensus building for national data harmonization.",
        "nomination_deadline": "July 10, 2026",
        "prerequisites": "Cadre rank of Director / Joint Director or above."
    }
]

# -------------------------------------------------------------------------
# 3. Hybrid AI Recommendation Engine Class
# -------------------------------------------------------------------------
class RecommendationEngine:
    def __init__(self):
        self.igot_courses = IGOT_COURSES
        self.tpac_programmes = NSSTA_TPAC_PROGRAMMES

    def recommend_for_officer(self, officer_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes an officer profile with skill_gaps and computes:
        1. Top prioritized iGOT micro-courses (Stage 1: Urgent, Stage 2: Applied, Stage 3: Strategic).
        2. Top matched NSSTA TPAC Flagship Programmes.
        3. Projected Competency Uplift score (+X%).
        """
        skill_gaps = officer_profile.get("skill_gaps", {})
        cadre = officer_profile.get("cadre", "")
        role_key = officer_profile.get("role_key", "")
        division = officer_profile.get("division_code", "")

        # Score each iGOT course
        scored_courses = []
        for course in self.igot_courses:
            score = 0.0
            primary_c = course["primary_competency"]
            gap_info = skill_gaps.get(primary_c, {})
            gap_val = gap_info.get("gap", 0)

            # Base score from primary competency gap
            score += gap_val * 40.0
            if gap_val >= 2:
                score += 30.0  # High severity priority boost
                
            # Explicitly boost if this course's primary competency is in the officer's top priority gaps
            top_gaps = officer_profile.get("top_priority_gaps", [])
            if any(g.get("id") == primary_c for g in top_gaps):
                score += 150.0 # Massive boost to ensure it surfaces in Stage 1

            # Secondary competency match
            for sec_c in course.get("competency_tags", []):
                sec_gap = skill_gaps.get(sec_c, {}).get("gap", 0)
                score += sec_gap * 15.0

            # Division bonus
            if (division == "NAD" and "STAT-02" in course["competency_tags"]) or \
               (division == "ESD" and ("STAT-03" in course["competency_tags"] or "STAT-04" in course["competency_tags"])) or \
               (division == "SSD" and "STAT-05" in course["competency_tags"]) or \
               (division == "FOD" and ("STAT-01" in course["competency_tags"] or "LEAD-02" in course["competency_tags"])) or \
               (division == "DIID" and ("TECH-01" in course["competency_tags"] or "TECH-07" in course["competency_tags"])):
                score += 25.0

            # Level fit
            level = course["level"]
            if "SAG" in role_key or "JAG" in role_key:
                if level in ["Advanced", "Executive"]: score += 15.0
            elif "STS" in role_key or "JTS" in role_key:
                if level in ["Intermediate", "Advanced"]: score += 15.0
            else:
                if level in ["Foundation", "Intermediate"]: score += 15.0

            # Estimated competency boost
            estimated_boost = round(gap_val * 1.8 + len(course["competency_tags"]) * 0.6, 1)

            scored_courses.append({
                **course,
                "match_score": round(score, 1),
                "targeted_gap_unit": primary_c,
                "targeted_gap_name": gap_info.get("name", primary_c),
                "gap_severity": gap_info.get("severity", "None"),
                "estimated_uplift_pct": max(1.2, estimated_boost),
                "enrolment_status": "Recommended"
            })

        scored_courses.sort(key=lambda x: x["match_score"], reverse=True)

        # Categorize into 3 Learning Pathway Stages
        stage1_urgent = [c for c in scored_courses if c["gap_severity"] == "High"][:3]
        if len(stage1_urgent) < 2:
            stage1_urgent = scored_courses[:2]
            
        stage2_applied = [c for c in scored_courses if c not in stage1_urgent and c["match_score"] > 20][:3]
        if not stage2_applied:
            stage2_applied = scored_courses[2:5]

        stage3_strategic = [c for c in scored_courses if c not in stage1_urgent and c not in stage2_applied][:3]

        # Score NSSTA TPAC Programmes
        matched_tpac = []
        for prog in self.tpac_programmes:
            t_score = 0.0
            for comp in prog["primary_competencies"]:
                gap_val = skill_gaps.get(comp, {}).get("gap", 0)
                t_score += gap_val * 35.0

            # Cadre matching
            for t_cadre in prog["target_cadres"]:
                if (cadre in t_cadre) or (role_key.split("_")[1] in t_cadre):
                    t_score += 30.0

            matched_tpac.append({
                **prog,
                "suitability_score": round(t_score, 1),
                "nomination_status": "Eligible for MoSPI Nomination" if t_score > 40 else "Available"
            })

        matched_tpac.sort(key=lambda x: x["suitability_score"], reverse=True)

        # Calculate projected index uplift if top 3 courses are completed
        top_uplift = sum(c["estimated_uplift_pct"] for c in stage1_urgent[:3])
        current_index = officer_profile.get("overall_competency_index", 75.0)
        projected_index = min(100.0, round(current_index + top_uplift, 1))

        return {
            "officer_id": officer_profile.get("officer_id"),
            "officer_name": officer_profile.get("name"),
            "current_competency_index": current_index,
            "projected_competency_index": projected_index,
            "potential_gain_pct": round(projected_index - current_index, 1),
            "learning_pathway": {
                "stage_1_urgent_gap_closure": stage1_urgent,
                "stage_2_applied_modernization": stage2_applied,
                "stage_3_leadership_strategic": stage3_strategic
            },
            "all_recommended_courses": scored_courses,
            "nssta_tpac_flagship_programmes": matched_tpac[:4]
        }

    def save_all_catalogs(self):
        with open(os.path.join(DATA_DIR, "igot_course_catalog.json"), "w") as f:
            json.dump(self.igot_courses, f, indent=2)
        with open(os.path.join(DASHBOARD_DATA_DIR, "igot_course_catalog.json"), "w") as f:
            json.dump(self.igot_courses, f, indent=2)

        with open(os.path.join(DATA_DIR, "nssta_tpac_catalog.json"), "w") as f:
            json.dump(self.tpac_programmes, f, indent=2)
        with open(os.path.join(DASHBOARD_DATA_DIR, "nssta_tpac_catalog.json"), "w") as f:
            json.dump(self.tpac_programmes, f, indent=2)

        # Generate recommendation for primary learner
        primary_path = os.path.join(DASHBOARD_DATA_DIR, "primary_learner.json")
        if os.path.exists(primary_path):
            with open(primary_path, "r") as f:
                primary = json.load(f)
            rec = self.recommend_for_officer(primary)
            with open(os.path.join(DASHBOARD_DATA_DIR, "primary_recommendations.json"), "w") as f:
                json.dump(rec, f, indent=2)
            with open(os.path.join(DATA_DIR, "primary_recommendations.json"), "w") as f:
                json.dump(rec, f, indent=2)

        print("[OK] Saved iGOT & NSSTA TPAC course catalogs and generated personalized recommendation pathways.")

if __name__ == "__main__":
    rec_engine = RecommendationEngine()
    rec_engine.save_all_catalogs()
