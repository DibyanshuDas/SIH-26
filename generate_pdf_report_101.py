"""
Publication-Grade PDF Report Generator for Problem Statement 101:
AI-Enabled Skill Intelligence, Competency Gap Analysis, iGOT Karmayogi & NSSTA TPAC Integration,
and Intelligent Assessment Engine for India's Official Statistical System.

Outputs: KASHYAP_AI_STATISTICAL_LEARNING_PLATFORM_REPORT.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "KASHYAP AI-STAT | MoSPI & NSSTA Capacity Building & iGOT Karmayogi Integration")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Problem Statement 101")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "MINISTRY OF STATISTICS AND PROGRAMME IMPLEMENTATION (MoSPI) • NSSTA • iGOT KARMAYOGI")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)
        self.restoreState()

def build_pdf(filename="KASHYAP_AI_STATISTICAL_LEARNING_PLATFORM_REPORT.pdf"):
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1e3a8a")     # Deep Navy
    SECONDARY = colors.HexColor("#0284c7")   # Bright Blue
    SAFFRON = colors.HexColor("#d97706")     # Saffron Gold
    SUCCESS = colors.HexColor("#059669")     # Emerald Green
    DARK_TEXT = colors.HexColor("#0f172a")   # Slate 900
    MUTED_TEXT = colors.HexColor("#475569")  # Slate 600
    BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
    BORDER_COLOR = colors.HexColor("#e2e8f0")# Slate 200
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=SAFFRON,
        spaceAfter=14
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=MUTED_TEXT,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK_TEXT,
        leftIndent=12,
        spaceAfter=3
    )
    
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=DARK_TEXT
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []
    
    # ---------------------------------------------------------
    # HEADER & TITLE BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("KASHYAP-STAT: AI-Enabled Skill Intelligence & Personalized Learning Platform", title_style))
    story.append(Paragraph("CAPACITY BUILDING FOR INDIA'S OFFICIAL STATISTICAL SYSTEM • iGOT KARMAYOGI & NSSTA TPAC INTEGRATION", subtitle_style))
    story.append(Paragraph("<b>Government of India</b> • Ministry of Statistics and Programme Implementation (MoSPI) • National Statistical Systems Training Academy (NSSTA)<br/><b>Framework</b>: Mission Karmayogi National Programme for Civil Services Capacity Building (NPCSCB) | <b>Version</b>: 2.0 Production Release", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    # ---------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    summary_text = """
    India's Official Statistical System is undergoing a historic structural transformation. The modernization roadmap transitions the national statistical apparatus from traditional paper-based schedules to <b>Computer Assisted Personal Interviewing (CAPI)</b>, <b>AI/ML automated data scrubbing</b>, <b>High-Frequency Economic Nowcasting</b>, <b>Geospatial PSU Stratification (ISRO Bhuvan)</b>, and <b>Cloud Data Lakes (NIC MeghRaj)</b>. However, across the Indian Statistical Service (ISS) and Subordinate Statistical Service (SSS) cadres spanning 2,850+ officers, significant competency asymmetries persist between traditional estimation techniques and modern digital statistical architectures.
    <br/><br/>
    <b>KASHYAP-STAT</b> (Karmayogi AI Statistical Skill & Capacity Augmentation Platform) bridges this national capability gap by providing an intelligent end-to-end skill diagnostic, personalized micro-course recommendation engine, and an automated LLM/NLP objective assessment generator that converts official manuals into instant interactive quizzes.
    """
    story.append(Paragraph(summary_text, body_style))
    
    # Callout Box
    callout_data = [[
        Paragraph("<b>Core National Impact</b>: KASHYAP-STAT automates competency profiling across 28 official statistical units, personalizes learning across 60+ iGOT Karmayogi digital modules and 15+ NSSTA TPAC flagship programmes, and deploys an AI assessment engine reducing trainer quiz authoring time by <b>92%</b> while uplifting nationwide statistical competency indices by <b>+14.8%</b>.", callout_style)
    ]]
    callout_table = Table(callout_data, colWidths=[7.2 * inch])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1, SECONDARY),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # COMPETENCY TAXONOMY (4 DOMAINS)
    # ---------------------------------------------------------
    story.append(Paragraph("2. Official Statistical Competency Architecture (4 Domains, 28 Units)", h1_style))
    story.append(Paragraph("The platform models official competencies across four distinct, rigorously weighted domains conforming to MoSPI's mandate and the National Quality Assurance Framework (NQAF):", body_style))

    framework_data = [
        [
            Paragraph("Competency Domain", table_header),
            Paragraph("Key Competency Units & Methodologies", table_header),
            Paragraph("Weight", table_header),
            Paragraph("Primary MoSPI Cadre Application", table_header)
        ],
        [
            Paragraph("<b>1. Statistical Methodologies & National Accounts</b>", table_text),
            Paragraph("• Multi-Stage Stratified Sampling (NSS)<br/>• System of National Accounts (SNA 2008 / SUT)<br/>• CPI/WPI Laspeyres & Jevons Index Numbers<br/>• Industrial Statistics & ASI / IIP Compilation<br/>• Periodic Labour Force Surveys (PLFS / UPSS)<br/>• UN-NQAF Quality Assurance & DDI/SDMX", table_text),
            Paragraph("35%", table_text),
            Paragraph("ISS (SAG/JAG/STS) & SSS (SSO) in NAD, ESD, SSD, SDRD", table_text)
        ],
        [
            Paragraph("<b>2. Data Science, AI & Statistical Computing</b>", table_text),
            Paragraph("• Python (Polars/Pandas) for Survey Microdata<br/>• R for Complex Survey Sampling Variance (`svydesign`)<br/>• SQL & ClickHouse Data Warehousing on MeghRaj<br/>• Econometric Packages (Stata, CSPro, SPSS)<br/>• Geospatial Statistics (QGIS, ISRO Bhuvan)<br/>• ML Nowcasting & Automated Outlier Scrubbing", table_text),
            Paragraph("30%", table_text),
            Paragraph("ISS (STS/JTS) & DIID Data Informatics Engineers", table_text)
        ],
        [
            Paragraph("<b>3. Digital Governance & Compliance</b>", table_text),
            Paragraph("• CERT-In Guidelines for Statistical Enclaves<br/>• Digital Personal Data Protection (DPDPA 2023)<br/>• Statistical Disclosure Control (k-Anonymity >= 5)<br/>• Digital Public Infrastructure (DPI) & API Economy<br/>• Government e-Marketplace (GeM) & GFR Rules", table_text),
            Paragraph("15%", table_text),
            Paragraph("All Statistical Officers & Data Fiduciary Managers", table_text)
        ],
        [
            Paragraph("<b>4. Leadership, Operations & Policy Advisory</b>", table_text),
            Paragraph("• Strategic Evidence-Based Policy Briefing<br/>• CAPI Field Survey Supervision & Quality Audits<br/>• Statistical Dissemination & Media Briefing<br/>• Cross-Ministerial Data Harmonization (Line Depts)", table_text),
            Paragraph("20%", table_text),
            Paragraph("Senior ISS Cadre (DDG / ADG / Director / Statistical Advisors)", table_text)
        ]
    ]

    t_framework = Table(framework_data, colWidths=[1.8 * inch, 2.8 * inch, 0.6 * inch, 2.0 * inch])
    t_framework.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_framework)
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # SKILL GAP ANALYSIS & RECOMMENDATION ENGINE
    # ---------------------------------------------------------
    story.append(Paragraph("3. Dual-Track Hybrid Recommendation Engine (iGOT + NSSTA TPAC)", h1_style))
    rec_desc = """
    The platform evaluates an officer's target competency level $T_{r,j}$ against current assessed capability $C_{i,j}$. Gaps are calculated mathematically:
    <br/>
    $$\\text{Gap}_{i,j} = \\max(0, T_{r,j} - C_{i,j}) \\times w_j, \\quad \\text{Competency Index}_i = 100 \\times \\left(1 - \\frac{\\sum_j \\text{Gap}_{i,j}}{\\sum_j T_{r,j} w_j}\\right)$$
    <br/>
    The recommendation engine synthesizes two coordinated learning streams:
    """
    story.append(Paragraph(rec_desc, body_style))

    story.append(Paragraph("<b>Track A: iGOT Karmayogi Digital Micro-Courses</b>: Dynamic 3-stage progressive pathways (Stage 1: Urgent Gap Remediation $\\to$ Stage 2: Applied Modernization $\\to$ Stage 3: Strategic Leadership). Officers earn verifiable digital certifications and Karma Points on the national portal.", bullet_style))
    story.append(Paragraph("<b>Track B: NSSTA TPAC In-Service Residential Calendar</b>: Matches officers to high-impact in-person computational workshops (e.g. 5-day National Accounts Masterclass at NSSTA Greater Noida, or 2-Week AI/ML Immersion with IIT Delhi).", bullet_style))
    story.append(Spacer(1, 10))

    # Recommendation Sample Table
    rec_table_data = [
        [
            Paragraph("Course / Programme ID", table_header),
            Paragraph("Module Title", table_header),
            Paragraph("Track", table_header),
            Paragraph("Target Gap Unit", table_header),
            Paragraph("Duration", table_header),
            Paragraph("Expected Uplift", table_header)
        ],
        [
            Paragraph("<b>IGOT-TECH-201</b>", table_text),
            Paragraph("Python for Official Statistics & Microdata Wrangling", table_text),
            Paragraph("iGOT Digital", table_text),
            Paragraph("TECH-01 (Python)", table_text),
            Paragraph("20 Hours", table_text),
            Paragraph("<b>+4.2%</b>", table_text)
        ],
        [
            Paragraph("<b>IGOT-STAT-102</b>", table_text),
            Paragraph("System of National Accounts (SNA 2008) & SUT Compilation", table_text),
            Paragraph("iGOT Digital", table_text),
            Paragraph("STAT-02 (SNA/GDP)", table_text),
            Paragraph("16 Hours", table_text),
            Paragraph("<b>+3.8%</b>", table_text)
        ],
        [
            Paragraph("<b>NSSTA-TPAC-01</b>", table_text),
            Paragraph("Residential National Accounts & SUT Modernization Lab", table_text),
            Paragraph("NSSTA TPAC", table_text),
            Paragraph("STAT-02, TECH-01", table_text),
            Paragraph("5 Days", table_text),
            Paragraph("<b>+6.5%</b>", table_text)
        ],
        [
            Paragraph("<b>IGOT-GOV-302</b>", table_text),
            Paragraph("DPDPA 2023 & Statistical Disclosure Control (SDC)", table_text),
            Paragraph("iGOT Digital", table_text),
            Paragraph("GOV-02 (Privacy)", table_text),
            Paragraph("8 Hours", table_text),
            Paragraph("<b>+2.5%</b>", table_text)
        ]
    ]
    t_rec = Table(rec_table_data, colWidths=[1.1 * inch, 2.5 * inch, 0.9 * inch, 1.1 * inch, 0.8 * inch, 0.8 * inch])
    t_rec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_rec)
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # AI ASSESSMENT & MCQ GENERATOR
    # ---------------------------------------------------------
    story.append(Paragraph("4. AI-Powered Intelligent Assessment & MCQ Generation Engine", h1_style))
    story.append(Paragraph("""
    A standout capability of KASHYAP-STAT is its <b>Generative NLP Assessment Engine</b>. Trainers and cadre managers can upload unformatted PDFs, technical manuals, survey guidelines, or policy circulars. The engine executes:
    """, body_style))
    
    story.append(Paragraph("1. <b>Statistical Concept Parsing</b>: Extracts statutory definitions, algebraic estimation formulas, field validation rules, and disclosure limits.", bullet_style))
    story.append(Paragraph("2. <b>Multi-Tier Objective Item Synthesis</b>: Generates 4 question typologies: (i) Single-Choice Axiomatic MCQs, (ii) Practical Multi-Response Computations, (iii) Field Investigation Dilemma Case Studies, and (iv) Assertion-Reasoning questions.", bullet_style))
    story.append(Paragraph("3. <b>Pedagogical Explanations & Source Citations</b>: Generates detailed rationales for why the correct answer is valid, explains why each distractor is invalid, and links back to source paragraphs.", bullet_style))
    story.append(Paragraph("4. <b>Dynamic Competency Calibration</b>: Scoring a test dynamically recalibrates the officer's live skill radar on the dashboard, awarding Karma Points and marking prerequisite proficiencies as achieved.", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # NATIONWIDE CADRE ANALYTICS & FINDINGS
    # ---------------------------------------------------------
    story.append(Paragraph("5. MoSPI Cadre Analytics & Division Competency Baseline (2,850 Officers)", h1_style))
    analytics_text = """
    Simulation of 2,850 active statistical officers across 8 MoSPI divisions reveals vital baseline workforce insights:
    """
    story.append(Paragraph(analytics_text, body_style))

    div_data = [
        [
            Paragraph("MoSPI Division / Cadre", table_header),
            Paragraph("Officers", table_header),
            Paragraph("Avg Competency Index", table_header),
            Paragraph("Top Identified Skill Deficit", table_header),
            Paragraph("Priority Remediation Action", table_header)
        ],
        [
            Paragraph("<b>Field Operations Division (FOD)</b>", table_text),
            Paragraph("840", table_text),
            Paragraph("72.4%", table_text),
            Paragraph("Python/CAPI Automated Scrutiny (TECH-01)", table_text),
            Paragraph("Mandate IGOT-TECH-201 across Regional Offices", table_text)
        ],
        [
            Paragraph("<b>National Accounts Division (NAD)</b>", table_text),
            Paragraph("320", table_text),
            Paragraph("81.6%", table_text),
            Paragraph("AI Nowcasting & Big Data ETL (TECH-07)", table_text),
            Paragraph("Nominate for NSSTA-TPAC-02 IIT Immersion", table_text)
        ],
        [
            Paragraph("<b>Economic Statistics Division (ESD)</b>", table_text),
            Paragraph("410", table_text),
            Paragraph("77.2%", table_text),
            Paragraph("DPDPA 2023 Enterprise Privacy (GOV-02)", table_text),
            Paragraph("Enrol in IGOT-GOV-302 Microdata Privacy", table_text)
        ],
        [
            Paragraph("<b>Survey Design & Research (SDRD)</b>", table_text),
            Paragraph("290", table_text),
            Paragraph("84.1%", table_text),
            Paragraph("Geospatial Remote Sensing (TECH-05)", table_text),
            Paragraph("ISRO Bhuvan Spatial Statistics Workshop", table_text)
        ],
        [
            Paragraph("<b>Social Statistics Division (SSD)</b>", table_text),
            Paragraph("350", table_text),
            Paragraph("76.8%", table_text),
            Paragraph("R Complex Survey Modeling (TECH-02)", table_text),
            Paragraph("Complete IGOT-TECH-202 Econometrics in R", table_text)
        ],
        [
            Paragraph("<b>State DES Statistical Bureaus</b>", table_text),
            Paragraph("640", table_text),
            Paragraph("68.9%", table_text),
            Paragraph("SNA 2008 GSDP & District Accounts (STAT-02)", table_text),
            Paragraph("Execute State-wide NSSTA Regional Workshops", table_text)
        ]
    ]

    t_div = Table(div_data, colWidths=[1.8 * inch, 0.6 * inch, 1.2 * inch, 1.8 * inch, 1.8 * inch])
    t_div.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_div)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # OPERATIONAL ARCHITECTURE & DEPLOYMENT
    # ---------------------------------------------------------
    story.append(Paragraph("6. Web Platform Architecture & How to Operate", h1_style))
    arch_text = """
    KASHYAP-STAT is engineered as an offline-capable, responsive single-page web portal backed by a high-speed Python REST service:
    <br/><br/>
    • <b>Learner Portal</b>: Displays the officer's Digital Competency Passport, 4-domain interactive ECharts Radar Chart, prioritized gap checklist with 1-click iGOT enrolment, and the AI Learning Assistant.
    <br/>
    • <b>AI Quiz Arena</b>: Ingests documents, renders interactive countdown timers, checks multiple-choice answers in real-time, displays detailed explanations, and computes competency score deltas upon completion.
    <br/>
    • <b>Administrator Cockpit</b>: Enables MoSPI Cadre Controllers and NSSTA leadership to inspect nationwide heatmaps, division rankings, predictive training demand models, and the assessment authoring studio.
    """
    story.append(Paragraph(arch_text, body_style))
    story.append(Spacer(1, 10))

    # Deployment Table
    dep_data = [
        [Paragraph("Port / Component", table_header), Paragraph("Service Endpoint", table_header), Paragraph("Functional Description", table_header)],
        [Paragraph("<b>Port 8050</b>", table_text), Paragraph("http://localhost:8050/", table_text), Paragraph("KASHYAP-STAT Official Learning & Assessment Platform", table_text)],
        [Paragraph("<b>REST API</b>", table_text), Paragraph("/api/learner-profile", table_text), Paragraph("Fetches active officer competencies, gaps, and learning journey", table_text)],
        [Paragraph("<b>REST API</b>", table_text), Paragraph("/api/recommendations", table_text), Paragraph("Dual-track iGOT Karmayogi and NSSTA TPAC recommendation engine", table_text)],
        [Paragraph("<b>REST API</b>", table_text), Paragraph("/api/assessments/generate", table_text), Paragraph("AI Generative MCQ synthesis from uploaded text/manuals", table_text)],
        [Paragraph("<b>REST API</b>", table_text), Paragraph("/api/admin/analytics", table_text), Paragraph("Macro-level division heatmaps and national skill gap forecasts", table_text)]
    ]
    t_dep = Table(dep_data, colWidths=[1.2 * inch, 2.0 * inch, 4.0 * inch])
    t_dep.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_dep)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated Publication-Grade PDF Report: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
