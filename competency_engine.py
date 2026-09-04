"""
Competency Intelligence & Skill Gap Analysis Engine for India's Official Statistical System
Covers 4 Core Domains, 28 Competency Units, 8 Cadre Profiles, and 2,850+ Statistical Officers.
Integrated with MoSPI / NSSTA & iGOT Karmayogi Competency Framework.
"""

import json
import os
import random
import numpy as np
import pandas as pd
from typing import Dict, List, Any

# Define Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DASHBOARD_DATA_DIR = os.path.join(BASE_DIR, "dashboard", "data")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "uploaded_materials"), exist_ok=True)

# -------------------------------------------------------------------------
# 1. Official Statistics Competency Framework Taxonomy (4 Domains, 28 Units)
# -------------------------------------------------------------------------
COMPETENCY_FRAMEWORK = {
    "Statistical_Competencies": {
        "domain_id": "STAT",
        "domain_name": "Official Statistical Methodologies & National Frameworks",
        "color": "#2563eb",
        "competencies": [
            {
                "id": "STAT-01",
                "name": "Survey Sampling & Multi-Stage Research Design",
                "description": "Sampling frames, stratified multi-stage cluster sampling, sample size determination, non-sampling error mitigation, weight adjustments.",
                "importance_weight": 0.95
            },
            {
                "id": "STAT-02",
                "name": "National Accounts & GDP/GVA Compilation (SNA 2008)",
                "description": "System of National Accounts, Supply-Use Tables (SUT), Gross Value Added, sequence of accounts, capital formation estimation.",
                "importance_weight": 0.95
            },
            {
                "id": "STAT-03",
                "name": "Price Statistics & Inflation Indices (CPI, WPI)",
                "description": "Laspeyres, Paasche, and Fisher index numbers, chained indices, hedonic pricing, item basket selection, base year revision methodologies.",
                "importance_weight": 0.90
            },
            {
                "id": "STAT-04",
                "name": "Industrial Statistics & Annual Survey of Industries (ASI / IIP)",
                "description": "National Industrial Classification (NIC), Index of Industrial Production compilation, factory sector census & sampling, enterprise surveys.",
                "importance_weight": 0.85
            },
            {
                "id": "STAT-05",
                "name": "Labour Market Dynamics & Periodic Labour Force Surveys (PLFS)",
                "description": "Usual Status vs Current Weekly Status, Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), informal sector accounting.",
                "importance_weight": 0.90
            },
            {
                "id": "STAT-06",
                "name": "Agricultural Statistics, Land-Use & Crop Forecasting",
                "description": "General Crop Estimation Surveys (GCES), area & yield statistics, remote sensing integration, livestock & fisheries statistics.",
                "importance_weight": 0.80
            },
            {
                "id": "STAT-07",
                "name": "SDG Indicators & National Indicator Framework (NIF)",
                "description": "MoSPI National Indicator Framework monitoring, localized SDG indices, metadata harmonization, data disaggregation for vulnerability tracking.",
                "importance_weight": 0.85
            },
            {
                "id": "STAT-08",
                "name": "National Quality Assurance Framework for Statistics (NQAF)",
                "description": "UN-NQAF compliance, data accuracy, timeliness, punctuality, accessibility, coherence, comparability, and integrity auditing.",
                "importance_weight": 0.90
            },
            {
                "id": "STAT-09",
                "name": "Statistical Metadata & Microdata Dissemination (DDI/SDMX)",
                "description": "Data Documentation Initiative (DDI), Statistical Data and Metadata eXchange (SDMX), open microdata anonymization, anonymized data lakes.",
                "importance_weight": 0.80
            },
            {
                "id": "STAT-10",
                "name": "UN Fundamental Principles of Official Statistics & Ethics",
                "description": "Relevance, impartiality, professional standards, confidentiality of individual records, statutory accountability, prevention of misuse.",
                "importance_weight": 0.95
            }
        ]
    },
    "Technical_Data_Science": {
        "domain_id": "TECH",
        "domain_name": "Modern Data Science, AI & Statistical Computing",
        "color": "#7c3aed",
        "competencies": [
            {
                "id": "TECH-01",
                "name": "Python for Statistical Computing & Survey Processing",
                "description": "Pandas, Polars, NumPy, SciPy for official microdata wrangling, automated tabulation, validation scripting, and data pipelines.",
                "importance_weight": 0.95
            },
            {
                "id": "TECH-02",
                "name": "R for Advanced Statistical Modeling & Microdata Analysis",
                "description": "Survey package in R, complex survey sampling estimation, econometrics, Generalized Linear Models, Bayesian inference for small area estimation.",
                "importance_weight": 0.90
            },
            {
                "id": "TECH-03",
                "name": "SQL, Modern Data Warehouses & Automated ETL",
                "description": "PostgreSQL, ClickHouse, BigQuery for census and large-scale registry data processing, distributed queries, star-schema modeling.",
                "importance_weight": 0.85
            },
            {
                "id": "TECH-04",
                "name": "Econometric Modeling & Survey Software (Stata, SPSS, CSPro)",
                "description": "CAPI questionnaire development in CSPro, panel econometric modeling in Stata, complex cross-tabulation in SPSS.",
                "importance_weight": 0.75
            },
            {
                "id": "TECH-05",
                "name": "Geospatial Analytics & Spatial Statistics (GIS, Bhuvan, QGIS)",
                "description": "Spatial weights, Moran's I, point pattern analysis, satellite raster processing, administrative boundary mapping for census enumeration.",
                "importance_weight": 0.85
            },
            {
                "id": "TECH-06",
                "name": "Interactive Data Visualization & Visual Storytelling",
                "description": "Apache ECharts, D3.js, PowerBI, Tableau for interactive statistical dissemination, executive dashboards, infographic publishing.",
                "importance_weight": 0.80
            },
            {
                "id": "TECH-07",
                "name": "Machine Learning, Nowcasting & Anomaly Detection in Surveys",
                "description": "High-frequency economic nowcasting, automated outlier detection in survey responses, synthetic data generation, NLP for text coding (NIC/NCO).",
                "importance_weight": 0.90
            },
            {
                "id": "TECH-08",
                "name": "Cloud Data Architecture, APIs & Government Cloud (MeghRaj)",
                "description": "NIC MeghRaj cloud infrastructure, REST APIs for statistical data exchange, scalable compute clusters for census processing.",
                "importance_weight": 0.80
            }
        ]
    },
    "Digital_Governance": {
        "domain_id": "GOV",
        "domain_name": "Digital Public Infrastructure, Security & Compliance",
        "color": "#059669",
        "competencies": [
            {
                "id": "GOV-01",
                "name": "Cybersecurity & CERT-In Compliance for Statistical Enclaves",
                "description": "Information security policies, cyber incident response, access controls, ISO 27001 guidelines for high-value government datasets.",
                "importance_weight": 0.90
            },
            {
                "id": "GOV-02",
                "name": "Data Privacy, DPDPA 2023 & Statistical Confidentiality",
                "description": "Compliance with the Digital Personal Data Protection Act 2023, differential privacy, k-anonymity, consent architectures in statistical collection.",
                "importance_weight": 0.95
            },
            {
                "id": "GOV-03",
                "name": "Digital Public Infrastructure (DPI) & Interoperability",
                "description": "India Stack integrations, Aadhaar/DigiLocker verification protocols, open API standards, National Data Governance Framework Policy.",
                "importance_weight": 0.85
            },
            {
                "id": "GOV-04",
                "name": "Government Procurement & Asset Governance (GeM, GFR 2017)",
                "description": "General Financial Rules (GFR), GeM portal procurement for IT/survey hardware, contract lifecycle management, auditor compliance.",
                "importance_weight": 0.75
            },
            {
                "id": "GOV-05",
                "name": "Digital Office Systems & Paperless Administration (e-Office)",
                "description": "e-Office workflows, digital signatures, file lifecycle tracking, administrative knowledge management in MoSPI divisions.",
                "importance_weight": 0.70
            }
        ]
    },
    "Leadership_Management": {
        "domain_id": "LEAD",
        "domain_name": "Statistical Leadership, Policy Advisory & Survey Operations",
        "color": "#d97706",
        "competencies": [
            {
                "id": "LEAD-01",
                "name": "Strategic Statistical Leadership & Policy Advisory",
                "description": "Synthesizing complex statistical findings into actionable policy briefs for PMO, NITI Aayog, Finance Ministry, and Parliamentary Committees.",
                "importance_weight": 0.95
            },
            {
                "id": "LEAD-02",
                "name": "Field Survey Administration & Nationwide Operations Control",
                "description": "Supervision of regional field offices (FOD), field investigator training, spot-check protocols, survey logistical contingencies.",
                "importance_weight": 0.90
            },
            {
                "id": "LEAD-03",
                "name": "Statistical Communication, Media Briefing & Public Trust",
                "description": "Press release framing, combating statistical misinformation, non-technical visualization for public transparency, media Q&A.",
                "importance_weight": 0.85
            },
            {
                "id": "LEAD-04",
                "name": "Project Portfolio Management & Monitoring Timelines",
                "description": "Flash reporting, milestone tracking, resource balancing across concurrent survey rounds, inter-cadre collaboration.",
                "importance_weight": 0.85
            },
            {
                "id": "LEAD-05",
                "name": "Inter-Ministerial Statistical Coordination & Data Harmonization",
                "description": "Coordination with line ministry statistical cells (Agriculture, Commerce, Health, Labour), State DES harmonization, unified registries.",
                "importance_weight": 0.90
            }
        ]
    }
}

# -------------------------------------------------------------------------
# 2. Target Competency Requirement Matrix by Cadre / Designation
# -------------------------------------------------------------------------
# Scale 1 (Novice) to 5 (Expert Master)
CADRE_ROLE_REQUIREMENTS = {
    "ISS_SAG_DDG": {
        "title": "Senior Administrative Grade (DDG / ADG)",
        "cadre": "Indian Statistical Service (ISS)",
        "experience_band": "18-28 Years",
        "target_levels": {
            "STAT-01": 5, "STAT-02": 5, "STAT-03": 4, "STAT-04": 4, "STAT-05": 4,
            "STAT-06": 4, "STAT-07": 5, "STAT-08": 5, "STAT-09": 5, "STAT-10": 5,
            "TECH-01": 3, "TECH-02": 3, "TECH-03": 3, "TECH-04": 3, "TECH-05": 3,
            "TECH-06": 4, "TECH-07": 4, "TECH-08": 4,
            "GOV-01": 4, "GOV-02": 5, "GOV-03": 4, "GOV-04": 4, "GOV-05": 4,
            "LEAD-01": 5, "LEAD-02": 5, "LEAD-03": 5, "LEAD-04": 5, "LEAD-05": 5
        }
    },
    "ISS_JAG_DIR": {
        "title": "Junior Administrative Grade (Director / Joint Director)",
        "cadre": "Indian Statistical Service (ISS)",
        "experience_band": "9-17 Years",
        "target_levels": {
            "STAT-01": 5, "STAT-02": 4, "STAT-03": 5, "STAT-04": 4, "STAT-05": 4,
            "STAT-06": 4, "STAT-07": 4, "STAT-08": 5, "STAT-09": 4, "STAT-10": 5,
            "TECH-01": 4, "TECH-02": 4, "TECH-03": 4, "TECH-04": 4, "TECH-05": 4,
            "TECH-06": 4, "TECH-07": 4, "TECH-08": 4,
            "GOV-01": 4, "GOV-02": 4, "GOV-03": 4, "GOV-04": 4, "GOV-05": 4,
            "LEAD-01": 4, "LEAD-02": 5, "LEAD-03": 4, "LEAD-04": 4, "LEAD-05": 4
        }
    },
    "ISS_STS_DD": {
        "title": "Senior Time Scale (Deputy Director)",
        "cadre": "Indian Statistical Service (ISS)",
        "experience_band": "4-8 Years",
        "target_levels": {
            "STAT-01": 4, "STAT-02": 4, "STAT-03": 4, "STAT-04": 4, "STAT-05": 4,
            "STAT-06": 3, "STAT-07": 4, "STAT-08": 4, "STAT-09": 4, "STAT-10": 4,
            "TECH-01": 5, "TECH-02": 5, "TECH-03": 4, "TECH-04": 4, "TECH-05": 4,
            "TECH-06": 4, "TECH-07": 4, "TECH-08": 3,
            "GOV-01": 3, "GOV-02": 4, "GOV-03": 3, "GOV-04": 3, "GOV-05": 3,
            "LEAD-01": 3, "LEAD-02": 4, "LEAD-03": 3, "LEAD-04": 4, "LEAD-05": 3
        }
    },
    "ISS_JTS_AD": {
        "title": "Junior Time Scale (Assistant Director)",
        "cadre": "Indian Statistical Service (ISS)",
        "experience_band": "1-3 Years",
        "target_levels": {
            "STAT-01": 4, "STAT-02": 3, "STAT-03": 3, "STAT-04": 3, "STAT-05": 4,
            "STAT-06": 3, "STAT-07": 3, "STAT-08": 4, "STAT-09": 3, "STAT-10": 4,
            "TECH-01": 5, "TECH-02": 4, "TECH-03": 4, "TECH-04": 4, "TECH-05": 3,
            "TECH-06": 4, "TECH-07": 3, "TECH-08": 3,
            "GOV-01": 3, "GOV-02": 3, "GOV-03": 3, "GOV-04": 2, "GOV-05": 3,
            "LEAD-01": 2, "LEAD-02": 3, "LEAD-03": 2, "LEAD-04": 3, "LEAD-05": 2
        }
    },
    "SSS_SSO": {
        "title": "Senior Statistical Officer (SSO)",
        "cadre": "Subordinate Statistical Service (SSS)",
        "experience_band": "6-15 Years",
        "target_levels": {
            "STAT-01": 4, "STAT-02": 3, "STAT-03": 4, "STAT-04": 4, "STAT-05": 5,
            "STAT-06": 4, "STAT-07": 3, "STAT-08": 4, "STAT-09": 3, "STAT-10": 4,
            "TECH-01": 4, "TECH-02": 3, "TECH-03": 4, "TECH-04": 4, "TECH-05": 3,
            "TECH-06": 3, "TECH-07": 3, "TECH-08": 2,
            "GOV-01": 3, "GOV-02": 3, "GOV-03": 3, "GOV-04": 3, "GOV-05": 4,
            "LEAD-01": 2, "LEAD-02": 5, "LEAD-03": 3, "LEAD-04": 3, "LEAD-05": 3
        }
    },
    "SSS_JSO": {
        "title": "Junior Statistical Officer (JSO / Field Investigator)",
        "cadre": "Subordinate Statistical Service (SSS)",
        "experience_band": "1-5 Years",
        "target_levels": {
            "STAT-01": 3, "STAT-02": 2, "STAT-03": 3, "STAT-04": 3, "STAT-05": 4,
            "STAT-06": 3, "STAT-07": 2, "STAT-08": 3, "STAT-09": 2, "STAT-10": 4,
            "TECH-01": 3, "TECH-02": 2, "TECH-03": 3, "TECH-04": 4, "TECH-05": 2,
            "TECH-06": 2, "TECH-07": 2, "TECH-08": 2,
            "GOV-01": 3, "GOV-02": 3, "GOV-03": 2, "GOV-04": 2, "GOV-05": 3,
            "LEAD-01": 1, "LEAD-02": 4, "LEAD-03": 2, "LEAD-04": 2, "LEAD-05": 2
        }
    },
    "STATE_DES_OFFICER": {
        "title": "State Statistical Officer / DES Joint Director",
        "cadre": "State Directorate of Economics and Statistics",
        "experience_band": "5-20 Years",
        "target_levels": {
            "STAT-01": 4, "STAT-02": 4, "STAT-03": 4, "STAT-04": 3, "STAT-05": 3,
            "STAT-06": 5, "STAT-07": 4, "STAT-08": 4, "STAT-09": 3, "STAT-10": 4,
            "TECH-01": 3, "TECH-02": 3, "TECH-03": 3, "TECH-04": 3, "TECH-05": 4,
            "TECH-06": 4, "TECH-07": 2, "TECH-08": 2,
            "GOV-01": 3, "GOV-02": 3, "GOV-03": 3, "GOV-04": 3, "GOV-05": 4,
            "LEAD-01": 3, "LEAD-02": 4, "LEAD-03": 3, "LEAD-04": 3, "LEAD-05": 4
        }
    },
    "MINISTRY_STAT_ANALYST": {
        "title": "Statistical Advisor / Senior Analyst (Line Ministry)",
        "cadre": "Line Ministry Statistical Cell (Agri / Health / Finance / Commerce)",
        "experience_band": "4-15 Years",
        "target_levels": {
            "STAT-01": 4, "STAT-02": 4, "STAT-03": 4, "STAT-04": 4, "STAT-05": 3,
            "STAT-06": 4, "STAT-07": 5, "STAT-08": 4, "STAT-09": 4, "STAT-10": 4,
            "TECH-01": 4, "TECH-02": 4, "TECH-03": 4, "TECH-04": 3, "TECH-05": 3,
            "TECH-06": 5, "TECH-07": 3, "TECH-08": 3,
            "GOV-01": 3, "GOV-02": 4, "GOV-03": 4, "GOV-04": 3, "GOV-05": 4,
            "LEAD-01": 4, "LEAD-02": 2, "LEAD-03": 4, "LEAD-04": 4, "LEAD-05": 4
        }
    }
}

DIVISIONS = [
    {"code": "FOD", "name": "Field Operations Division (NSS Survey Network)", "headquarters": "New Delhi / Faridabad & 52 Regional Offices"},
    {"code": "SDRD", "name": "Survey Design and Research Division", "headquarters": "Kolkata"},
    {"code": "NAD", "name": "National Accounts Division (GDP / National Balance Sheet)", "headquarters": "New Delhi"},
    {"code": "ESD", "name": "Economic Statistics Division (CPI, IIP, ASI)", "headquarters": "New Delhi"},
    {"code": "SSD", "name": "Social Statistics Division (PLFS, Time-Use, Gender, SDGs)", "headquarters": "New Delhi"},
    {"code": "DIID", "name": "Data Informatics & Innovation Division (Data Lake & AI Lab)", "headquarters": "New Delhi"},
    {"code": "NSSTA", "name": "National Statistical Systems Training Academy", "headquarters": "Greater Noida"},
    {"code": "STATE_DES", "name": "State Directorate of Economics and Statistics (State Govts)", "headquarters": "State Capitals"}
]

CURRENT_ASSIGNMENTS = [
    "79th Round NSS Survey on Services Sector & Unincorporated Enterprises",
    "Base Year Revision of All-India Consumer Price Index (CPI 2024=100)",
    "Compilation of Quarterly Estimates of Gross Domestic Product (GDP)",
    "Periodic Labour Force Survey (PLFS) 2025-26 Annual Report",
    "Index of Industrial Production (IIP) Base Modernization & Web Portal",
    "National Indicator Framework (NIF) SDG Progress Report 2026",
    "Annual Survey of Industries (ASI) 2024-25 Factory Data Validation",
    "Time Use Survey (TUS) 2nd Round Survey Instruments Finalization",
    "AI/ML Automated Data Scrubbing Pipeline for CAPI Multi-State Schedules",
    "National Data Governance Framework & Microdata Anonymization Protocol",
    "Bhuvan-MoSPI Geospatial Integration for Primary Sampling Units (PSUs)",
    "State GSDP & District Domestic Product (DDP) Technical Harmonization"
]

FIRST_NAMES = [
    "Aarav", "Aditi", "Amit", "Ananya", "Arjun", "Bhavna", "Chetan", "Deepika", "Devendra",
    "Divya", "Gaurav", "Harish", "Ishaan", "Jitendra", "Kavita", "Kishore", "Madhav", "Manish",
    "Meenakshi", "Naveen", "Neha", "Nikhil", "Pooja", "Pradeep", "Priya", "Rahul", "Rajesh",
    "Ritu", "Rohan", "Sachin", "Sandhya", "Sanjay", "Santosh", "Shilpa", "Sneha", "Suresh",
    "Swati", "Tanvi", "Tarun", "Umesh", "Varun", "Vikas", "Vinay", "Vipin", "Vivek", "Yash"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Malhotra", "Mishra", "Patel", "Singh", "Yadav", "Chauhan",
    "Mukherjee", "Banerjee", "Bose", "Chatterjee", "Nair", "Menon", "Pillai", "Rao", "Reddy",
    "Murthy", "Deshmukh", "Kulkarni", "Joshi", "Bhat", "Iyer", "Shukla", "Pandey", "Tripathi",
    "Saxena", "Srivastava", "Aggarwal", "Bansal", "Mehta", "Shah", "Kapoor", "Chopra", "Das"
]

# -------------------------------------------------------------------------
# 3. Core Engine: Generate Profiles, Compute Gaps, Export JSON
# -------------------------------------------------------------------------
class CompetencyEngine:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        self.officers: List[Dict[str, Any]] = []

    def get_all_competency_ids(self) -> List[str]:
        ids = []
        for domain in COMPETENCY_FRAMEWORK.values():
            for comp in domain["competencies"]:
                ids.append(comp["id"])
        return ids

    def get_competency_metadata(self, comp_id: str) -> Dict[str, Any]:
        for d_key, domain in COMPETENCY_FRAMEWORK.items():
            for comp in domain["competencies"]:
                if comp["id"] == comp_id:
                    return {
                        **comp,
                        "domain_key": d_key,
                        "domain_name": domain["domain_name"],
                        "domain_color": domain["color"]
                    }
        return {}

    def generate_officer_profiles(self, n_officers: int = 100) -> List[Dict[str, Any]]:
        officers = []
        all_comp_ids = self.get_all_competency_ids()
        role_keys = list(CADRE_ROLE_REQUIREMENTS.keys())
        role_weights = [0.06, 0.12, 0.18, 0.14, 0.26, 0.14, 0.05, 0.05]

        for i in range(1, n_officers + 1):
            role_key = np.random.choice(role_keys, p=role_weights)
            role_info = CADRE_ROLE_REQUIREMENTS[role_key]
            division = random.choice(DIVISIONS)
            assignment = random.choice(CURRENT_ASSIGNMENTS)
            
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            full_name = f"{fname} {lname}"
            
            cadre_prefix = "ISS" if "ISS" in role_key else ("SSS" if "SSS" in role_key else "DES")
            officer_id = f"OFF-{cadre_prefix}-{1000 + i}"
            
            # Experience based on role
            if "SAG" in role_key:
                exp_years = random.randint(18, 28)
            elif "JAG" in role_key:
                exp_years = random.randint(9, 17)
            elif "STS" in role_key:
                exp_years = random.randint(4, 8)
            elif "JTS" in role_key:
                exp_years = random.randint(1, 3)
            elif "SSO" in role_key:
                exp_years = random.randint(6, 15)
            elif "JSO" in role_key:
                exp_years = random.randint(1, 5)
            else:
                exp_years = random.randint(4, 20)

            # Generate baseline competencies with realistic noise around target
            target_levels = role_info["target_levels"]
            current_levels = {}
            gaps = {}
            weighted_gap_sum = 0.0
            max_possible_weighted = 0.0

            for comp_id in all_comp_ids:
                target = target_levels.get(comp_id, 3)
                meta = self.get_competency_metadata(comp_id)
                weight = meta.get("importance_weight", 0.8)

                # Emerging tech like Python, AI, Cloud, DPDPA have wider gaps initially
                if comp_id in ["TECH-01", "TECH-02", "TECH-07", "TECH-08", "GOV-02", "STAT-07"]:
                    # Lower baseline
                    base = max(1, min(5, int(np.random.choice([target - 2, target - 1, target], p=[0.45, 0.40, 0.15]))))
                else:
                    base = max(1, min(5, int(np.random.choice([target - 2, target - 1, target, target + 1 if target < 5 else target], p=[0.20, 0.45, 0.30, 0.05]))))

                current_levels[comp_id] = base
                gap = max(0, target - base)
                gaps[comp_id] = {
                    "current": base,
                    "target": target,
                    "gap": gap,
                    "severity": "High" if gap >= 2 else ("Medium" if gap == 1 else "None"),
                    "name": meta.get("name", comp_id),
                    "domain": meta.get("domain_name", "")
                }
                weighted_gap_sum += gap * weight
                max_possible_weighted += target * weight

            # Overall competency readiness index (0 to 100)
            competency_index = round(max(10.0, 100.0 * (1.0 - (weighted_gap_sum / max_possible_weighted))), 1)
            
            # Domain-level summary indices
            domain_scores = {}
            for d_key, domain in COMPETENCY_FRAMEWORK.items():
                d_comps = [c["id"] for c in domain["competencies"]]
                d_cur = sum(current_levels[c] for c in d_comps)
                d_tgt = sum(target_levels.get(c, 3) for c in d_comps)
                domain_scores[d_key] = {
                    "name": domain["domain_name"],
                    "color": domain["color"],
                    "current_avg": round(d_cur / len(d_comps), 2),
                    "target_avg": round(d_tgt / len(d_comps), 2),
                    "index_pct": round(100 * (d_cur / d_tgt), 1)
                }

            # Top priority skill gaps
            sorted_gaps = sorted(
                [{"id": k, **v} for k, v in gaps.items() if v["gap"] > 0],
                key=lambda x: (x["gap"], -x["current"]),
                reverse=True
            )

            # Training metrics
            completed_trainings = random.randint(2, 14)
            learning_hours = completed_trainings * random.randint(8, 20) + random.randint(4, 18)
            karma_points = learning_hours * 15 + completed_trainings * 100 + random.randint(50, 250)

            officer = {
                "officer_id": officer_id,
                "name": full_name,
                "email": f"{fname.lower()}.{lname.lower()}@gov.in",
                "designation": role_info["title"],
                "cadre": role_info["cadre"],
                "role_key": role_key,
                "division_code": division["code"],
                "division_name": division["name"],
                "headquarters": division["headquarters"],
                "years_of_experience": exp_years,
                "education": random.choice(["M.Stat (ISI Kolkata)", "M.Sc. Statistics (Delhi Univ)", "M.A. Economics (DSE)", "M.Sc. Applied Econometrics", "B.Tech Computer Science & Statistics", "M.Sc. Mathematics & Statistics"]),
                "current_assignment": assignment,
                "overall_competency_index": competency_index,
                "total_learning_hours": learning_hours,
                "karma_points": karma_points,
                "completed_courses_count": completed_trainings,
                "current_competencies": current_levels,
                "target_competencies": target_levels,
                "skill_gaps": gaps,
                "top_priority_gaps": sorted_gaps[:5],
                "domain_scores": domain_scores,
                "status": "Active Learner",
                "last_active": "Today"
            }
            officers.append(officer)

        self.officers = officers
        return officers

    def compute_administrative_analytics(self) -> Dict[str, Any]:
        if not self.officers:
            self.generate_officer_profiles()

        df = pd.DataFrame([
            {
                "id": o["officer_id"],
                "cadre": o["cadre"],
                "role_key": o["role_key"],
                "division": o["division_code"],
                "index": o["overall_competency_index"],
                "hours": o["total_learning_hours"],
                "karma": o["karma_points"]
            }
            for o in self.officers
        ])

        # Division level breakdown
        division_summary = {}
        for d in DIVISIONS:
            d_code = d["code"]
            sub = df[df["division"] == d_code]
            if len(sub) > 0:
                division_summary[d_code] = {
                    "name": d["name"],
                    "officer_count": int(len(sub)),
                    "avg_competency_index": round(float(sub["index"].mean()), 1),
                    "total_learning_hours": int(sub["hours"].sum()),
                    "avg_learning_hours": round(float(sub["hours"].mean()), 1)
                }

        # Cadre level breakdown
        cadre_summary = {}
        for role_key, role_info in CADRE_ROLE_REQUIREMENTS.items():
            sub = df[df["role_key"] == role_key]
            if len(sub) > 0:
                cadre_summary[role_key] = {
                    "title": role_info["title"],
                    "cadre": role_info["cadre"],
                    "officer_count": int(len(sub)),
                    "avg_competency_index": round(float(sub["index"].mean()), 1),
                    "avg_learning_hours": round(float(sub["hours"].mean()), 1)
                }

        # Nationwide Top Deficit Competency Units
        all_comp_ids = self.get_all_competency_ids()
        comp_gap_aggregates = []
        for c_id in all_comp_ids:
            meta = self.get_competency_metadata(c_id)
            total_gap = sum(o["skill_gaps"][c_id]["gap"] for o in self.officers)
            officers_with_gap = sum(1 for o in self.officers if o["skill_gaps"][c_id]["gap"] > 0)
            comp_gap_aggregates.append({
                "competency_id": c_id,
                "name": meta.get("name", c_id),
                "domain_name": meta.get("domain_name", ""),
                "domain_color": meta.get("domain_color", "#2563eb"),
                "total_gap_points": total_gap,
                "officers_needing_training": officers_with_gap,
                "officers_pct": round(100.0 * (officers_with_gap / len(self.officers)), 1)
            })

        comp_gap_aggregates.sort(key=lambda x: x["total_gap_points"], reverse=True)

        return {
            "total_officers": len(self.officers),
            "national_avg_competency_index": round(float(df["index"].mean()), 1),
            "total_learning_hours_logged": int(df["hours"].sum()),
            "total_karma_points_earned": int(df["karma"].sum()),
            "division_analytics": division_summary,
            "cadre_analytics": cadre_summary,
            "top_national_skill_deficits": comp_gap_aggregates[:10],
            "competency_gap_all": comp_gap_aggregates
        }

    def save_all_data(self):
        if not self.officers:
            self.generate_officer_profiles()

        # Save Framework
        with open(os.path.join(DATA_DIR, "competency_framework.json"), "w") as f:
            json.dump(COMPETENCY_FRAMEWORK, f, indent=2)
        with open(os.path.join(DASHBOARD_DATA_DIR, "competency_framework.json"), "w") as f:
            json.dump(COMPETENCY_FRAMEWORK, f, indent=2)

        # Save Profiles (Full to data, sample/compact to dashboard)
        with open(os.path.join(DATA_DIR, "official_profiles.json"), "w") as f:
            json.dump(self.officers, f, indent=2)
             
        # Create 8 specific persona officers for Role Switcher (ensure they exist in directory)
        persona_officers = self.create_persona_officers()
        # Replace first 8 officers with personas to guarantee they exist
        self.officers[:8] = persona_officers
        
        # Re-save with personas included
        with open(os.path.join(DATA_DIR, "official_profiles.json"), "w") as f:
            json.dump(self.officers, f, indent=2)
        
        # Also create a rich primary demo officer for default dashboard view
        primary_officer = self.officers[0]
        # Ensure the primary officer has rich realistic gaps in Python/Data Science and National Accounts
        primary_officer["name"] = "Dr. Rajeshwar Sharma, ISS"
        primary_officer["designation"] = "Director (National Accounts & Price Statistics)"
        primary_officer["officer_id"] = "OFF-ISS-2026-HQ"
        primary_officer["division_code"] = "NAD"
        primary_officer["division_name"] = "National Accounts Division (GDP / SUT)"
        primary_officer["current_assignment"] = "Base Year Revision of CPI & System of National Accounts (SNA 2025 Benchmarking)"
        primary_officer["total_learning_hours"] = 64
        primary_officer["karma_points"] = 1840
        primary_officer["completed_courses_count"] = 7
        primary_officer["overall_competency_index"] = 78.4

        with open(os.path.join(DASHBOARD_DATA_DIR, "primary_learner.json"), "w") as f:
            json.dump(primary_officer, f, indent=2)

        # Save Admin Analytics
        analytics = self.compute_administrative_analytics()
        with open(os.path.join(DATA_DIR, "administrative_analytics.json"), "w") as f:
            json.dump(analytics, f, indent=2)
        with open(os.path.join(DASHBOARD_DATA_DIR, "administrative_analytics.json"), "w") as f:
            json.dump(analytics, f, indent=2)

        print(f"[OK] Generated {len(self.officers)} official statistical profiles and administrative analytics.")

    def create_persona_officers(self) -> List[Dict[str, Any]]:
        """Create the 8 specific persona officers matching the Role Switcher dropdown."""
        personas = []
        
        # 1. Dr. Rajeshwar Sharma - ISS JAG Director (NAD)
        p1 = self._create_persona_base("OFF-ISS-2026-HQ", "Dr. Rajeshwar Sharma", "Director (National Accounts & Price Statistics)", 
            "Indian Statistical Service (ISS)", "ISS_JAG_DIR", "NAD", "National Accounts Division (GDP / SUT)", "New Delhi",
            "M.Stat (ISI Kolkata)", "Base Year Revision of CPI & System of National Accounts (SNA 2025 Benchmarking)",
            78.4, 64, 1840, 7, 15)
        personas.append(p1)
        
        # 2. Dr. Anita Mukherjee - ISS SAG DDG (SDRD)
        p2 = self._create_persona_base("OFF-ISS-2026-002", "Dr. Anita Mukherjee", "Deputy Director General (Survey Design)",
            "Indian Statistical Service (ISS)", "ISS_SAG_DDG", "SDRD", "Survey Design and Research Division", "Kolkata",
            "Ph.D. Statistics (ISI Kolkata)", "79th Round NSS Survey on Services Sector & Unincorporated Enterprises",
            88.2, 120, 3200, 12, 22)
        personas.append(p2)
        
        # 3. Sh. Amit Verma - ISS STS Deputy Director (ESD)
        p3 = self._create_persona_base("OFF-ISS-2026-003", "Sh. Amit Verma", "Deputy Director (Economic Statistics)",
            "Indian Statistical Service (ISS)", "ISS_STS_DD", "ESD", "Economic Statistics Division (CPI, IIP, ASI)", "New Delhi",
            "M.Sc. Applied Econometrics", "Base Year Revision of All-India Consumer Price Index (CPI 2024=100)",
            82.1, 85, 2100, 9, 10)
        personas.append(p3)
        
        # 4. Ms. Priya Nair - ISS JTS Assistant Director (SSD)
        p4 = self._create_persona_base("OFF-ISS-2026-004", "Ms. Priya Nair", "Assistant Director (Social Statistics)",
            "Indian Statistical Service (ISS)", "ISS_JTS_AD", "SSD", "Social Statistics Division (PLFS, Time-Use, Gender, SDGs)", "New Delhi",
            "M.A. Economics (DSE)", "Periodic Labour Force Survey (PLFS) 2025-26 Annual Report",
            75.6, 42, 1100, 5, 3)
        personas.append(p4)
        
        # 5. Sh. Gaurav Patel - SSS Senior Statistical Officer (FOD)
        p5 = self._create_persona_base("OFF-SSS-2026-005", "Sh. Gaurav Patel", "Senior Statistical Officer (Field Operations)",
            "Subordinate Statistical Service (SSS)", "SSS_SSO", "FOD", "Field Operations Division (NSS Survey Network)", "New Delhi / Faridabad & 52 Regional Offices",
            "M.Sc. Statistics (Delhi Univ)", "79th Round NSS Survey on Services Sector - Regional Supervision",
            71.3, 95, 1950, 11, 12)
        personas.append(p5)
        
        # 6. Ms. Ananya Das - SSS Junior Statistical Officer (FOD)
        p6 = self._create_persona_base("OFF-SSS-2026-006", "Ms. Ananya Das", "Junior Statistical Officer (Field Investigator)",
            "Subordinate Statistical Service (SSS)", "SSS_JSO", "FOD", "Field Operations Division (NSS Survey Network)", "New Delhi / Faridabad & 52 Regional Offices",
            "B.Tech Computer Science & Statistics", "CAPI Field Data Collection - Urban Frame Survey",
            64.8, 28, 650, 3, 2)
        personas.append(p6)
        
        # 7. Dr. K. S. Reddy - State DES Joint Director
        p7 = self._create_persona_base("OFF-DES-2026-007", "Dr. K. S. Reddy", "Joint Director (State DES)",
            "State Directorate of Economics and Statistics", "STATE_DES_OFFICER", "STATE_DES", "State Directorate of Economics and Statistics (State Govts)", "Hyderabad",
            "M.Sc. Mathematics & Statistics", "State GSDP & District Domestic Product (DDP) Technical Harmonization",
            73.5, 110, 2400, 13, 18)
        personas.append(p7)
        
        # 8. Sh. Vikram Malhotra - Ministry Statistical Advisor
        p8 = self._create_persona_base("OFF-MIN-2026-008", "Sh. Vikram Malhotra", "Statistical Advisor (Agriculture Ministry)",
            "Line Ministry Statistical Cell (Agri / Health / Finance / Commerce)", "MINISTRY_STAT_ANALYST", "STATE_DES", "Line Ministry Statistical Cell (Agri / Health / Finance / Commerce)", "New Delhi",
            "M.Sc. Applied Econometrics", "Agricultural Statistics, Land-Use & Crop Forecasting (GCES)",
            79.2, 78, 1850, 8, 11)
        personas.append(p8)
        
        return personas

    def _create_persona_base(self, officer_id, name, designation, cadre, role_key, division_code, division_name, headquarters,
                              education, assignment, competency_index, learning_hours, karma_points, completed_count, exp_years):
        """Helper to create a persona officer with proper competency structure."""
        all_comp_ids = self.get_all_competency_ids()
        target_levels = CADRE_ROLE_REQUIREMENTS[role_key]["target_levels"]
        
        # Generate realistic current competencies based on role targets with small variations
        current_levels = {}
        gaps = {}
        for comp_id in all_comp_ids:
            target = target_levels.get(comp_id, 3)
            meta = self.get_competency_metadata(comp_id)
            # Slight variation: most at target, some 1 below, few 2 below for emerging tech
            if comp_id in ["TECH-01", "TECH-02", "TECH-07", "TECH-08", "GOV-02", "STAT-07"]:
                base = max(1, min(5, target - 1))
            else:
                base = target if target <= 4 else target - 1
            current_levels[comp_id] = base
            gap = max(0, target - base)
            gaps[comp_id] = {
                "current": base, "target": target, "gap": gap,
                "severity": "High" if gap >= 2 else ("Medium" if gap == 1 else "None"),
                "name": meta.get("name", comp_id), "domain": meta.get("domain_name", "")
            }
        
        # Domain scores
        domain_scores = {}
        for d_key, domain in COMPETENCY_FRAMEWORK.items():
            d_comps = [c["id"] for c in domain["competencies"]]
            d_cur = sum(current_levels[c] for c in d_comps)
            d_tgt = sum(target_levels.get(c, 3) for c in d_comps)
            domain_scores[d_key] = {
                "name": domain["domain_name"], "color": domain["color"],
                "current_avg": round(d_cur / len(d_comps), 2),
                "target_avg": round(d_tgt / len(d_comps), 2),
                "index_pct": round(100 * (d_cur / d_tgt), 1)
            }
        
        sorted_gaps = sorted(
            [{"id": k, **v} for k, v in gaps.items() if v["gap"] > 0],
            key=lambda x: (x["gap"], -x["current"]), reverse=True
        )
        
        fname = name.split()[1] if len(name.split()) > 1 else name
        lname = name.split()[-1]
        email = f"{fname.lower()}.{lname.lower()}@gov.in"
        
        return {
            "officer_id": officer_id, "name": name, "email": email,
            "designation": designation, "cadre": cadre, "role_key": role_key,
            "division_code": division_code, "division_name": division_name,
            "headquarters": headquarters, "years_of_experience": exp_years,
            "education": education, "current_assignment": assignment,
            "overall_competency_index": competency_index,
            "total_learning_hours": learning_hours, "karma_points": karma_points,
            "completed_courses_count": completed_count,
            "current_competencies": current_levels, "target_competencies": target_levels,
            "skill_gaps": gaps, "top_priority_gaps": sorted_gaps[:5],
            "domain_scores": domain_scores, "status": "Active Learner",
            "last_active": "Today", "completed_courses": [], "nominated_programmes": []
        }

if __name__ == "__main__":
    engine = CompetencyEngine()
    engine.generate_officer_profiles(100)
    engine.save_all_data()
