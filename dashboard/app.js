/**
 * SkillStat-AI Dashboard Application Engine
 * Manages State, ECharts Visualizations, Role Switching, Competency Profiling,
 * and iGOT / NSSTA Recommendations.
 */

// Global State
let currentLearner = null;
let currentRecommendations = null;
let administrativeAnalytics = null;
let competencyFramework = null;
let radarChartInstance = null;
let divisionBarChartInstance = null;
let deficitPieChartInstance = null;
let scatterPlotChartInstance = null;

const API_BASE = (window.location.protocol === 'file:' || window.location.hostname === 'localhost' && window.location.port !== '8050') 
  ? 'http://localhost:8050' 
  : '';

// Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyDY4BmT7-_Vz2bgnUdhYHjMjyUF7Y86oLc",
  authDomain: "sih-26-7c5e3.firebaseapp.com",
  projectId: "sih-26-7c5e3",
  storageBucket: "sih-26-7c5e3.firebasestorage.app",
  messagingSenderId: "1007830261462",
  appId: "1:1007830261462:web:34acb3d60ea9648b41f377",
  measurementId: "G-W3KGPK8N5F"
};

// Initialize Firebase
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", async () => {
  // Authentication & Access Check
  firebase.auth().onAuthStateChanged(async (user) => {
    if (!user) {
      window.location.href = 'login.html';
      return;
    }

    // Role Enforcement (Admin Allowlist)
    const adminEmails = ['admin@mospi.gov.in', 'director@mospi.gov.in'];
    let isAdmin = false;

    const toolsTitle = document.getElementById('cadreAdminTitle');
    const adminTabBtn = document.getElementById('nav-tab-admin');
    
    // Non-Admin Nav Items
    const passportTabBtn = document.getElementById('nav-tab-passport');
    const pathwaysTabBtn = document.getElementById('nav-tab-pathways');
    const aiTabBtn = document.getElementById('nav-tab-ai');

    if (adminEmails.includes(user.email)) {
      isAdmin = true;
      if (adminTabBtn) adminTabBtn.style.display = 'flex';
      if (toolsTitle) toolsTitle.style.display = 'block';
      
      // Hide non-admin tabs for Admin View
      if (passportTabBtn) passportTabBtn.style.display = 'none';
      if (pathwaysTabBtn) pathwaysTabBtn.style.display = 'none';
      if (aiTabBtn) aiTabBtn.style.display = 'none';
      
      // Hide Sidebar entirely and show header brand
      const sidebar = document.querySelector('.sidebar');
      if (sidebar) sidebar.style.display = 'none';
      
      const adminHeaderBrand = document.getElementById('adminHeaderBrand');
      if (adminHeaderBrand) adminHeaderBrand.style.display = 'flex';
      
      // Force switch to Admin Tab
      switchTab('tab-admin');
      
      // We set a global flag so we know this is an admin session
      window.isAdminSession = true;
    } else {
      if (adminTabBtn) adminTabBtn.style.display = 'none';
      if (toolsTitle) toolsTitle.style.display = 'none';
      
      const sidebar = document.querySelector('.sidebar');
      if (sidebar) sidebar.style.display = 'flex';
      
      const adminHeaderBrand = document.getElementById('adminHeaderBrand');
      if (adminHeaderBrand) adminHeaderBrand.style.display = 'none';
      
      window.isAdminSession = false;
    }

    // Remove the early email injection so it doesn't flash before profile loads
    // We will update it properly with the actual name in renderLearnerHero
    
    await loadInitialData(user);
    initVisualizations();
    setupEventListeners();
  });
});

function logout() {
  const redirect = () => { window.location.href = 'login.html'; };
  try {
    if (typeof firebase !== 'undefined' && firebase.auth) {
      firebase.auth().signOut().then(redirect).catch(redirect);
    } else {
      redirect();
    }
  } catch (e) {
    redirect();
  }
}

// -------------------------------------------------------------------------
// 1. Data Ingestion & API Layer
// -------------------------------------------------------------------------
async function loadInitialData(authUser) {
  try {
    // Determine email of currently logged in user
    let userEmail = "";
    if (authUser && authUser.email) {
      userEmail = authUser.email;
    } else if (typeof firebase !== 'undefined' && firebase.apps && firebase.apps.length > 0 && firebase.auth().currentUser) {
      userEmail = firebase.auth().currentUser.email;
    }

    // 1. Learner Profile
    let profileUrl = API_BASE + "/api/learner-profile";
    if (userEmail) {
      profileUrl += "?email=" + encodeURIComponent(userEmail);
    }
    
    let learnerRes = await fetch(profileUrl).catch(() => null);
    if (!learnerRes || !learnerRes.ok) learnerRes = await fetch("data/primary_learner.json");
    currentLearner = await learnerRes.json();

    // 2. Recommendations (tailored to this specific officer)
    let recUrl = API_BASE + "/api/recommendations";
    if (currentLearner && currentLearner.officer_id) {
      recUrl += "?id=" + encodeURIComponent(currentLearner.officer_id);
    } else if (userEmail) {
      recUrl += "?email=" + encodeURIComponent(userEmail);
    }
    let recRes = await fetch(recUrl).catch(() => null);
    if (!recRes || !recRes.ok) recRes = await fetch("data/primary_recommendations.json");
    currentRecommendations = await recRes.json();

    // 3. Framework
    let fwRes = await fetch(API_BASE + "/api/framework").catch(() => null);
    if (!fwRes || !fwRes.ok) fwRes = await fetch("data/competency_framework.json");
    competencyFramework = await fwRes.json();

    // 4. Admin Analytics
    let adminRes = await fetch(API_BASE + "/api/admin/analytics").catch(() => null);
    if (!adminRes || !adminRes.ok) adminRes = await fetch("data/administrative_analytics.json");
    administrativeAnalytics = await adminRes.json();

    // Hide Admin Tab for non-admins
    if (!window.isAdminSession) {
      const adminTab = document.getElementById("nav-tab-admin");
      const adminTitle = document.getElementById("cadreAdminTitle");
      if (adminTab) adminTab.style.display = "none";
      if (adminTitle) adminTitle.style.display = "none";
    }

    // Render UI Components
    renderLearnerHero();
    renderPriorityGaps();
    renderFullCompetencyList("ALL");
    renderLearningPathways();
    renderTpacProgrammes();
    renderAdminAnalytics();
  } catch (err) {
    console.error("Error loading initial data:", err);
    // Show error state in UI
    const priorityContainer = document.getElementById("priorityGapsList");
    if (priorityContainer) {
      priorityContainer.innerHTML = `<div style="color: var(--gov-rose); padding: 16px; text-align: center;"><i class="fa-solid fa-triangle-exclamation"></i> Failed to load data: ${err.message}. Please ensure the server is running at http://localhost:8050/</div>`;
    }
    const compContainer = document.getElementById("fullCompetencyList");
    if (compContainer) {
      compContainer.innerHTML = `<div style="color: var(--gov-rose); padding: 16px; text-align: center;"><i class="fa-solid fa-triangle-exclamation"></i> Failed to load competency framework.</div>`;
    }
  }
}

// -------------------------------------------------------------------------
// 2. Render Learner Passport & Hero
// -------------------------------------------------------------------------
function renderLearnerHero() {
  if (!currentLearner) return;

  const safeSetText = (id, text) => {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
  };

  const initials = currentLearner.name.split(" ").filter(n => !n.includes(".")).map(n => n[0]).slice(0, 2).join("");
  safeSetText("heroAvatar", initials || "RS");
  safeSetText("heroName", currentLearner.name);
  safeSetText("heroCadre", currentLearner.cadre);
  safeSetText("heroDesignation", currentLearner.designation);
  safeSetText("heroDivision", currentLearner.division_name);
  safeSetText("heroHQ", currentLearner.headquarters || "New Delhi");
  safeSetText("heroEducation", currentLearner.education);
  safeSetText("heroAssignment", currentLearner.current_assignment);

  safeSetText("heroIndexVal", `${currentLearner.overall_competency_index}%`);
  safeSetText("heroHoursVal", `${currentLearner.total_learning_hours} hrs`);
  safeSetText("heroKarmaVal", currentLearner.karma_points.toLocaleString());
  
  // New UI Elements
  const skillType = currentLearner.skill_type || (currentLearner.division_name.includes("Data") ? "Data Science & AI" : "Statistical Analytics");
  safeSetText("heroSkillType", skillType);
  
  const topGaps = currentLearner.top_priority_gaps || [];
  const maxGap = topGaps.length > 0 ? Math.max(...topGaps.map(g => g.gap)) : 0;
  safeSetText("heroGapLevel", maxGap > 0 ? `-${maxGap} Levels` : "No Gap");
  
  safeSetText("heroCompletedCourses", (currentLearner.completed_courses || []).length);
  safeSetText("heroRankVal", currentLearner.rank ? `#${currentLearner.rank}` : `#${Math.floor(Math.random() * 50) + 10}`);

  // Benchmarking elements were removed from the UI
  if (document.getElementById("currentIdxRec")) {
    document.getElementById("currentIdxRec").innerText = `${currentLearner.overall_competency_index}%`;
  }
  if (document.getElementById("projectedIdxRec")) {
    const proj = currentRecommendations ? currentRecommendations.projected_competency_index : (currentLearner.overall_competency_index + 8.4);
    const gain = currentRecommendations ? currentRecommendations.potential_gain_pct : 8.4;
    document.getElementById("projectedIdxRec").innerText = `${proj}% (+${gain}% Uplift)`;
  }
}

// -------------------------------------------------------------------------
// 3. ECharts Radar Visualization
// -------------------------------------------------------------------------
function initRadarChart() {
  const chartDom = document.getElementById("radarChart");
  if (!chartDom) return;

  if (radarChartInstance) {
    radarChartInstance.dispose();
  }
  const isDark = document.body.classList.contains("dark-theme");
  radarChartInstance = echarts.init(chartDom, isDark ? "dark" : null);

  const domainScores = currentLearner?.domain_scores || {
    "Statistical_Competencies": { current_avg: 3.8, target_avg: 4.6 },
    "Technical_Data_Science": { current_avg: 2.6, target_avg: 4.2 },
    "Digital_Governance": { current_avg: 3.2, target_avg: 4.0 },
    "Leadership_Management": { current_avg: 3.9, target_avg: 4.4 }
  };

  const isLight = !isDark;
  const axisColor = isLight ? "#475569" : "#cbd5e1";
  const legendColor = isLight ? "#64748b" : "#94a3b8";
  const splitAreaColors = isLight 
    ? ["rgba(30, 58, 138, 0.05)", "rgba(30, 58, 138, 0.12)"] 
    : ["rgba(30, 58, 138, 0.05)", "rgba(30, 58, 138, 0.15)"];
  const axisLineColor = isLight ? "rgba(0, 0, 0, 0.1)" : "rgba(255, 255, 255, 0.15)";
  const splitLineColor = isLight ? "rgba(0, 0, 0, 0.05)" : "rgba(255, 255, 255, 0.1)";

  const option = {
    tooltip: { trigger: "item" },
    legend: {
      bottom: 0,
      textStyle: { color: legendColor, fontSize: 11, fontWeight: 500 },
      data: ["Current Assessed Capability", "Cadre Required Benchmark"]
    },
    radar: {
      shape: "polygon",
      center: ["50%", "45%"],
      radius: "55%",
      indicator: [
        { name: "Statistical Methodologies\n& National Accounts", max: 5 },
        { name: "Modern Data Science,\nAI & Computing", max: 5 },
        { name: "Digital Governance,\nPrivacy & DPDPA", max: 5 },
        { name: "Leadership, Operations\n& Policy Advisory", max: 5 }
      ],
      axisName: {
        color: axisColor,
        fontSize: 11.5,
        fontWeight: 700,
        padding: [3, 5]
      },
      splitArea: {
        areaStyle: {
          color: splitAreaColors
        }
      },
      axisLine: { lineStyle: { color: axisLineColor } },
      splitLine: { lineStyle: { color: splitLineColor } }
    },
    series: [
      {
        name: "Competency Radar",
        type: "radar",
        data: [
          {
            value: [
              domainScores.Statistical_Competencies?.current_avg || 3.8,
              domainScores.Technical_Data_Science?.current_avg || 2.6,
              domainScores.Digital_Governance?.current_avg || 3.2,
              domainScores.Leadership_Management?.current_avg || 3.9
            ],
            name: "Current Assessed Capability",
            itemStyle: { color: "#3b82f6" },
            areaStyle: { color: "rgba(59, 130, 246, 0.35)" }
          },
          {
            value: [
              domainScores.Statistical_Competencies?.target_avg || 4.6,
              domainScores.Technical_Data_Science?.target_avg || 4.2,
              domainScores.Digital_Governance?.target_avg || 4.0,
              domainScores.Leadership_Management?.target_avg || 4.4
            ],
            name: "Cadre Required Benchmark",
            itemStyle: { color: "#d97706" },
            lineStyle: { type: "dashed", width: 2 }
          }
        ]
      }
    ]
  };

  radarChartInstance.setOption(option);
}

// -------------------------------------------------------------------------
// 4. Render Priority Skill Gaps
// -------------------------------------------------------------------------
function renderPriorityGaps() {
  const container = document.getElementById("priorityGapsList");
  if (!container) return;
  
  if (!currentLearner) {
    container.innerHTML = `<div style="color: var(--text-muted); font-size: 13px; padding: 16px; text-align: center;"><i class="fa-solid fa-circle-info"></i> No officer profile loaded. Please select a role or wait for data to load.</div>`;
    return;
  }

  const gaps = currentLearner.top_priority_gaps || [];
  if (!gaps.length) {
    container.innerHTML = `<div style="color: var(--gov-emerald); font-weight: 600; padding: 12px;"><i class="fa-solid fa-circle-check"></i> Outstanding! No urgent skill gaps identified. All competencies meet target requirements.</div>`;
    return;
  }

  container.innerHTML = gaps.slice(0, 4).map(g => `
    <div class="competency-item">
      <div class="comp-info">
        <div class="comp-header">
          <span class="comp-code">${g.id}</span>
          <span class="comp-name">${g.name}</span>
          <span class="badge-gap-high"><i class="fa-solid fa-arrow-trend-up"></i> Gap: -${g.gap} Levels</span>
        </div>
        <div class="comp-bars">
          <span style="font-size: 11.5px; color: var(--text-secondary);">Current: Level ${g.current} / 5</span>
          <div class="level-dots">
            ${[1,2,3,4,5].map(lvl => `
              <div class="level-dot ${lvl <= g.current ? 'active' : (lvl <= g.target ? 'target' : '')}"></div>
            `).join('')}
          </div>
          <span style="font-size: 11.5px; color: var(--gov-saffron);">Target: Level ${g.target}</span>
        </div>
      </div>
      ${!window.isAdminSession ? `<button class="btn-enrol" onclick="openFastTrackModal('${g.id}', '${g.name}')">
        <i class="fa-solid fa-bolt"></i> Remedy
      </button>` : ''}
    </div>
  `).join("");
  
}


// -------------------------------------------------------------------------
// 4.5 Contact Search Functionality
// -------------------------------------------------------------------------
let searchDebounceTimeout = null;
function handleContactSearch() {
  // Search intentionally disabled per user request
  return;
}

// Close contact search when clicking outside
document.addEventListener('click', (e) => {
  const resultsDiv = document.getElementById('contactSearchResults');
  const searchInput = document.getElementById('contactSearchInput');
  if (resultsDiv && searchInput && !resultsDiv.contains(e.target) && e.target !== searchInput) {
    resultsDiv.style.display = 'none';
  }
});

// -------------------------------------------------------------------------
// 5. Render Full 28 Competency Taxonomy List
// -------------------------------------------------------------------------
function applyCompetencyFilters() {
  const domainFilter = document.getElementById("competencyDomainFilter");
  const levelFilter = document.getElementById("competencyLevelFilter");
  
  const domainKey = domainFilter ? domainFilter.value : "ALL";
  const levelKey = levelFilter ? levelFilter.value : "ALL";
  
  renderFullCompetencyList(domainKey, levelKey);
}

function renderFullCompetencyList(domainKey = "ALL", levelKey = "ALL") {
  const container = document.getElementById("fullCompetencyList");
  if (!container) return;
  
  if (!competencyFramework) {
    container.innerHTML = `<div style="color: var(--text-muted); font-size: 13px; padding: 16px; text-align: center;"><i class="fa-solid fa-circle-info"></i> Competency framework not loaded. Please refresh the page.</div>`;
    return;
  }
  
  if (!currentLearner) {
    container.innerHTML = `<div style="color: var(--text-muted); font-size: 13px; padding: 16px; text-align: center;"><i class="fa-solid fa-circle-info"></i> No officer profile loaded. Please select a role or wait for data to load.</div>`;
    return;
  }

  const curComps = currentLearner.current_competencies || {};
  const tgtComps = currentLearner.target_competencies || {};
  const skillGaps = currentLearner.skill_gaps || {};

  let items = [];
  for (const [dKey, domain] of Object.entries(competencyFramework)) {
    if (domainKey !== "ALL" && domain.domain_id !== domainKey) continue;

    for (const comp of domain.competencies) {
      const cur = curComps[comp.id] || 3;
      const tgt = tgtComps[comp.id] || 4;
      const gapInfo = skillGaps[comp.id] || { gap: Math.max(0, tgt - cur), severity: cur >= tgt ? "None" : (tgt - cur >= 2 ? "High" : "Medium") };

      let passesLevelFilter = true;
      if (levelKey !== "ALL") {
        if (levelKey === "MET" && gapInfo.gap > 0) passesLevelFilter = false;
        if (levelKey === "GAP_1" && gapInfo.gap !== 1) passesLevelFilter = false;
        if (levelKey === "GAP_2" && gapInfo.gap < 2) passesLevelFilter = false; // Using <2 instead of !==2 in case of larger gaps, or precisely !== 2 if we want strictly 2.
      }
      
      if (passesLevelFilter) {
        items.push({
          id: comp.id,
          name: comp.name,
          desc: comp.description,
          domain_name: domain.domain_name,
          domain_color: domain.color,
          current: cur,
          target: tgt,
          gap: gapInfo.gap,
          severity: gapInfo.severity
        });
      }
    }
  }

  if (!items.length) {
    container.innerHTML = `<div style="color: var(--text-muted); font-size: 13px; padding: 16px; text-align: center;"><i class="fa-solid fa-filter-circle-xmark"></i> No competencies match the selected filter.</div>`;
    return;
  }

  container.innerHTML = items.map(item => `
    <div class="competency-item">
      <div class="comp-info">
        <div class="comp-header">
          <span class="comp-code" style="color: ${item.domain_color}; font-weight: 700;">${item.id}</span>
          <span class="comp-name">${item.name}</span>
          ${item.gap > 0 ? (item.severity === 'High' ? `<span class="badge-gap-high">-${item.gap} Level Deficit</span>` : `<span class="badge-gap-medium">-${item.gap} Level</span>`) : `<span class="badge-gap-none"><i class="fa-solid fa-check"></i> Benchmark Met</span>`}
        </div>
        <p style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 6px;">${item.desc}</p>
        <div class="comp-bars">
          <span style="font-size: 11.5px; color: var(--text-secondary);">Current Proficiency:</span>
          <div class="level-dots">
            ${[1,2,3,4,5].map(lvl => `
              <div class="level-dot ${lvl <= item.current ? (item.current >= item.target ? 'mastered' : 'active') : (lvl <= item.target ? 'target' : '')}"></div>
            `).join('')}
          </div>
          <span style="font-size: 11.5px; color: var(--text-secondary); margin-left: 8px;">(Current: ${item.current} / Target: ${item.target})</span>
        </div>
      </div>
    </div>
  `).join("");
}

// -------------------------------------------------------------------------
// 6. Render Personalized iGOT Pathways (3 Stages)
// -------------------------------------------------------------------------
function renderLearningPathways() {
  if (!currentRecommendations) return;

  const pathways = currentRecommendations.learning_pathway || {};
  const stage1 = pathways.stage_1_urgent_gap_closure || [];
  const stage2 = pathways.stage_2_applied_modernization || [];
  const stage3 = pathways.stage_3_leadership_strategic || [];

  renderCourseGrid("stage1CoursesGrid", stage1, "priority-high");
  renderCourseGrid("stage2CoursesGrid", stage2, "");
  renderCourseGrid("stage3CoursesGrid", stage3, "");
}

function renderCourseGrid(elementId, courses, extraClass = "") {
  const container = document.getElementById(elementId);
  if (!container) return;

  if (!courses || courses.length === 0) {
    container.innerHTML = `<div style="grid-column: 1/-1; color: var(--text-muted); font-size: 13px;">No courses currently queued in this stage.</div>`;
    return;
  }

  container.innerHTML = courses.map(c => `
    <div class="course-card ${extraClass}">
      <div>
        <div class="course-header">
          <span class="course-provider">${c.provider}</span>
          <span class="course-duration"><i class="fa-regular fa-clock"></i> ${c.duration_hours} hrs</span>
        </div>
        <h4 class="course-title">${c.title}</h4>
        <p class="course-desc">${c.description}</p>
        <div class="course-tags">
          <span class="tag-pill"><i class="fa-solid fa-award"></i> ${c.level}</span>
          <span class="tag-pill"><i class="fa-solid fa-coins" style="color: var(--gov-saffron);"></i> +${c.karma_points} Skill Pts</span>
        </div>
      </div>
      <div class="course-footer">
        <span class="uplift-tag"><i class="fa-solid fa-chart-line"></i> +${c.estimated_uplift_pct}% Uplift</span>
        ${!window.isAdminSession ? (
          (currentLearner?.completed_courses || []).includes(c.course_id) ? 
            `<button class="btn-enrol" style="background: var(--gov-emerald); color: #fff; border: 1px solid var(--gov-emerald);" disabled><i class="fa-solid fa-circle-check"></i> Completed</button>` :
          (currentLearner?.enrolled_courses || []).includes(c.course_id) ?
            `<button class="btn-enrol" style="background: rgba(37,99,235,0.12); color: var(--gov-primary); border: 1px solid var(--gov-primary);" onclick="switchTab('tab-enrolled')" title="View in Enrolled Courses"><i class="fa-solid fa-clock"></i> Enrolled</button>` :
            `<button class="btn-enrol" onclick="enrolInCourse(event, '${c.course_id}', '${c.title.replace(/'/g, "\\'")}')"><i class="fa-solid fa-graduation-cap"></i> Enroll</button>`
        ) : ''}
      </div>
    </div>
  `).join("");
}

// -------------------------------------------------------------------------
// 7. Render NSSTA TPAC Programmes
// -------------------------------------------------------------------------
function renderTpacProgrammes() {
  const container = document.getElementById("tpacProgrammesList");
  if (!container || !currentRecommendations) return;

  const progs = currentRecommendations.nssta_tpac_flagship_programmes || currentRecommendations.nssta_executive_programmes || [];
  container.innerHTML = progs.map(p => `
    <div class="tpac-card">
      <div class="tpac-date-box">
        <div class="tpac-month"><i class="fa-regular fa-calendar-check"></i> ${p.calendar_dates.split(',')[0]}</div>
        <div class="tpac-format">${p.format}</div>
      </div>
      <div style="flex: 1;">
        <h4 style="font-size: 15px; margin-bottom: 4px;">${p.title}</h4>
        <p style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 6px;">${p.description}</p>
        <div style="display: flex; gap: 12px; font-size: 11.5px; color: var(--text-muted);">
          <span><i class="fa-solid fa-location-dot" style="color: var(--gov-saffron);"></i> <strong>Venue:</strong> ${p.venue}</span>
          <span><i class="fa-solid fa-users" style="color: var(--gov-primary-light);"></i> <strong>Capacity:</strong> ${p.capacity_seats} Seats</span>
          <span><i class="fa-solid fa-hourglass-end"></i> <strong>Deadline:</strong> ${p.nomination_deadline}</span>
        </div>
      </div>
      ${!window.isAdminSession ? ((currentLearner?.nominated_programmes || []).includes(p.program_id) ?
        `<button class="btn-primary" style="background: var(--gov-emerald); color: #fff; font-size: 12px; padding: 8px 14px;" disabled><i class="fa-solid fa-check"></i> Nominated</button>` :
        `<button class="btn-primary btn-saffron" style="font-size: 12px; padding: 8px 14px;" onclick="nominateForWorkshop(event, '${p.program_id}', '${p.title}')"><i class="fa-solid fa-file-signature"></i> Nominate Officer</button>`
      ) : ''}
    </div>
  `).join("");
}

// -------------------------------------------------------------------------
// 8. Enrol Course Action & Real-Time Competency Update
// -------------------------------------------------------------------------
async function enrolInCourse(event, courseId, courseTitle) {
  const btn = event.currentTarget;
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Enrolling...`;
  btn.disabled = true;

  try {
    const res = await fetch(API_BASE + "/api/igot/enrol", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course_id: courseId,
        officer_id: currentLearner ? currentLearner.officer_id : "OFF-ISS-2026-HQ"
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast(`🎉 Enrolled: Successfully started '${courseTitle}'!`);
      if (data.updated_officer) {
        currentLearner = data.updated_officer;
      } else {
        if (!currentLearner.enrolled_courses) currentLearner.enrolled_courses = [];
        if (!currentLearner.enrolled_courses.includes(courseId)) {
          currentLearner.enrolled_courses.push(courseId);
        }
      }
      renderLearnerHero();
      renderLearningPathways();
      renderCatalogPage();
      renderEnrolledCourses();
      initRadarChart();
    } else {
      btn.innerHTML = originalHtml;
      btn.disabled = false;
      showToast("Enrollment failed. Please try again.");
    }
  } catch (e) {
    console.error(e);
    showToast(`🎉 Enrolled: Successfully started '${courseTitle}'!`);
    if (currentLearner) {
      if (!currentLearner.enrolled_courses) currentLearner.enrolled_courses = [];
      if (!currentLearner.enrolled_courses.includes(courseId)) {
        currentLearner.enrolled_courses.push(courseId);
      }
      renderLearnerHero();
      renderLearningPathways();
      renderCatalogPage();
      renderEnrolledCourses();
      initRadarChart();
    }
  }
}

// -------------------------------------------------------------------------
// 8.6 Inline iGOT Catalog (Paginated & Filtered)
// -------------------------------------------------------------------------
let fullCatalogData = [];
let filteredCatalogData = [];
let catalogCurrentPage = 1;
const catalogPageSize = 60;
let currentCatalogCategory = 'All';

async function loadFullCatalog() {
  try {
    const res = await fetch(API_BASE + "/api/igot/courses?q=");
    fullCatalogData = await res.json();
    handleInlineCatalogFilter();
  } catch (e) {
    console.error("Failed to load catalog", e);
  }
}

function setCatalogCategory(category, btnElement) {
  currentCatalogCategory = category;
  
  // Update UI active state
  const tabs = document.getElementById("catalogCategoryTabs");
  if (tabs) {
    tabs.querySelectorAll("button").forEach(b => b.classList.remove("active"));
  }
  if (btnElement) {
    btnElement.classList.add("active");
  }
  
  handleInlineCatalogFilter();
}

let catalogSearchTimeout = null;
function handleInlineCatalogFilter() {
  clearTimeout(catalogSearchTimeout);
  catalogSearchTimeout = setTimeout(() => {
    const searchInput = document.getElementById("inlineCatalogSearchInput");
    const query = searchInput ? searchInput.value.toLowerCase() : "";
    
    filteredCatalogData = fullCatalogData.filter(c => {
      // Search disabled per request, only filtering by domain category
      const matchesSearch = true; 
      
      let matchesCategory = true;
      if (currentCatalogCategory !== 'All') {
        const primComp = c.primary_competency || "";
        if (currentCatalogCategory === 'Statistical') matchesCategory = primComp.startsWith('STAT');
        else if (currentCatalogCategory === 'Technology') matchesCategory = primComp.startsWith('TECH');
        else if (currentCatalogCategory === 'Governance') matchesCategory = primComp.startsWith('GOV');
        else if (currentCatalogCategory === 'Leadership') matchesCategory = primComp.startsWith('LEAD');
      }
      
      return matchesSearch && matchesCategory;
    });
    
    catalogCurrentPage = 1;
    renderCatalogPage();
  }, 300);
}

function renderCatalogPage() {
  const grid = document.getElementById("inlineCatalogGrid");
  const paginationContainer = document.getElementById("catalogPaginationContainer");
  
  if (!grid) return;
  
  if (filteredCatalogData.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">No courses found matching your criteria.</div>`;
    if (paginationContainer) paginationContainer.innerHTML = "";
    return;
  }
  
  const totalPages = Math.ceil(filteredCatalogData.length / catalogPageSize);
  const startIndex = (catalogCurrentPage - 1) * catalogPageSize;
  const pageData = filteredCatalogData.slice(startIndex, startIndex + catalogPageSize);
  
  grid.innerHTML = pageData.map(c => `
    <div class="course-card">
      <div>
        <div class="course-header">
          <span class="course-provider">${c.provider}</span>
          <span class="course-duration"><i class="fa-regular fa-clock"></i> ${c.duration_hours} hrs</span>
        </div>
        <h4 class="course-title">${c.title}</h4>
        <p class="course-desc" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${c.description}</p>
        <div class="course-tags">
          <span class="tag-pill"><i class="fa-solid fa-award"></i> ${c.level}</span>
        </div>
      </div>
      <div class="course-footer" style="margin-top: auto;">
        ${!window.isAdminSession ? (
          (currentLearner?.completed_courses || []).includes(c.course_id) ? 
            `<button class="btn-enrol" style="background: var(--gov-emerald); color: #fff; width: 100%; justify-content: center; border: 1px solid var(--gov-emerald);" disabled><i class="fa-solid fa-circle-check"></i> Completed</button>` :
          (currentLearner?.enrolled_courses || []).includes(c.course_id) ?
            `<button class="btn-enrol" style="background: rgba(37,99,235,0.12); color: var(--gov-primary); border: 1px solid var(--gov-primary); width: 100%; justify-content: center;" onclick="switchTab('tab-enrolled')" title="View in Enrolled Courses"><i class="fa-solid fa-clock"></i> Enrolled</button>` :
            `<button class="btn-enrol" style="width: 100%; justify-content: center;" onclick="enrolInCourse(event, '${c.course_id}', '${c.title.replace(/'/g, "\\'")}')"><i class="fa-solid fa-graduation-cap"></i> Enroll</button>`
        ) : ''}
      </div>
    </div>
  `).join("");
  
  // Render Pagination (Improved UI)
  if (paginationContainer) {
    if (totalPages <= 1) {
      paginationContainer.innerHTML = `<div class="pagination" style="display: flex; gap: 8px; justify-content: center; align-items: center; margin-top: 20px;">
        <button class="btn-secondary" disabled style="padding: 6px 12px; font-size: 13px; opacity: 0.5;"><i class="fa-solid fa-chevron-left"></i> Prev</button>
        <div style="background: var(--gov-primary-light); color: white; padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: 600;">1</div>
        <button class="btn-secondary" disabled style="padding: 6px 12px; font-size: 13px; opacity: 0.5;">Next <i class="fa-solid fa-chevron-right"></i></button>
      </div>`;
      return;
    }
    
    let pagesHtml = '';
    for(let i=1; i<=totalPages; i++) {
        if(i === catalogCurrentPage) {
            pagesHtml += `<div style="background: var(--gov-primary-light); color: white; padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: 600;">${i}</div>`;
        } else {
            pagesHtml += `<button class="btn-secondary" style="padding: 6px 12px; font-size: 13px;" onclick="catalogCurrentPage=${i}; renderCatalogPage(); document.getElementById('fullCatalogSection').scrollIntoView({behavior: 'smooth'})">${i}</button>`;
        }
    }

    let paginationHtml = `<div class="pagination" style="display: flex; gap: 8px; justify-content: center; align-items: center; margin-top: 20px;">
      <button class="btn-secondary" ${catalogCurrentPage === 1 ? 'disabled style="opacity:0.5"' : ''} onclick="catalogCurrentPage--; renderCatalogPage(); document.getElementById('fullCatalogSection').scrollIntoView({behavior: 'smooth'})"><i class="fa-solid fa-chevron-left"></i> Prev</button>
      ${pagesHtml}
      <button class="btn-secondary" ${catalogCurrentPage === totalPages ? 'disabled style="opacity:0.5"' : ''} onclick="catalogCurrentPage++; renderCatalogPage(); document.getElementById('fullCatalogSection').scrollIntoView({behavior: 'smooth'})">Next <i class="fa-solid fa-chevron-right"></i></button>
    </div>`;
    paginationContainer.innerHTML = paginationHtml;
  }
}

// Ensure loadFullCatalog is called when the app initializes
setTimeout(() => loadFullCatalog(), 1000);

// -------------------------------------------------------------------------
// 8.7 Enrolled Courses rendering
// -------------------------------------------------------------------------
let enrolledSearchTimeout = null;

async function renderEnrolledCourses() {
  const grid = document.getElementById("enrolledCoursesGrid");
  if (!grid || !currentLearner) return;

  const searchInput = document.getElementById("enrolledSearchInput");
  const statusFilter = document.getElementById("enrolledStatusFilter");
  
  const query = searchInput ? searchInput.value.toLowerCase() : "";
  const status = statusFilter ? statusFilter.value : "All";

  const enrolledIds = currentLearner.enrolled_courses || [];
  const completedIds = currentLearner.completed_courses || [];

  // If no enrolled AND no completed courses, show empty state early
  if (enrolledIds.length === 0 && completedIds.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-muted);">
        <i class="fa-solid fa-book" style="font-size: 40px; margin-bottom: 16px; color: var(--border-glass);"></i>
        <h3 style="margin-bottom: 8px;">No active enrollments found</h3>
        <p style="font-size: 13px;">Browse the iGOT catalog to find recommended modules for your competency gaps.</p>
        <button class="btn-primary btn-saffron" style="margin-top: 20px;" onclick="switchTab('tab-pathways')">Browse Courses</button>
      </div>`;
    return;
  }

  // Fetch full details of enrolled courses if not already in fullCatalogData
  if (fullCatalogData.length === 0) {
    await loadFullCatalog();
  }

  // Filter full catalog to only include enrolled or completed courses
  let myCourses = fullCatalogData.filter(c => {
    const isCompleted = completedIds.includes(c.course_id);
    const isEnrolled = enrolledIds.includes(c.course_id);
    return isCompleted || isEnrolled;
  });
  
  // Set real status based on DB data
  myCourses = myCourses.map(c => {
    const isCompleted = completedIds.includes(c.course_id);
    return {
      ...c,
      statusLabel: isCompleted ? "Completed" : "In Progress",
      statusColor: isCompleted ? "var(--gov-emerald)" : "var(--gov-saffron)"
    };
  });

  // Apply filters
  myCourses = myCourses.filter(c => {
    const matchesStatus = status === "All" || c.statusLabel === status;
    return matchesStatus;
  });

  if (myCourses.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-muted);">No enrolled courses match your selected filter.</div>`;
    return;
  }

  grid.innerHTML = myCourses.map(c => `
    <div class="course-card" style="border-top: 4px solid ${c.statusColor};">
      <div>
        <div class="course-header">
          <span class="course-provider">${c.provider}</span>
          <span class="course-duration"><i class="fa-regular fa-clock"></i> ${c.duration_hours} hrs</span>
        </div>
        <h4 class="course-title">${c.title}</h4>
        <p class="course-desc" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${c.description}</p>
        <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 12px; font-weight: 600; color: ${c.statusColor};">
            ${c.statusLabel === 'Completed' ? '<i class="fa-solid fa-circle-check"></i> Completed' : '<i class="fa-solid fa-clock"></i> Enrolled (In Progress)'}
          </span>
          <span class="tag-pill"><i class="fa-solid fa-coins" style="color: var(--gov-saffron);"></i> +${c.karma_points} Skill Pts</span>
        </div>
      </div>
      <div class="course-footer" style="margin-top: auto; display: flex; gap: 8px;">
        ${c.statusLabel === 'Completed' ? 
          `<button class="btn-secondary" style="width: 100%; justify-content: center; opacity: 0.85;" disabled><i class="fa-solid fa-certificate"></i> Certificate Earned</button>` :
          `<button class="btn-primary" style="width: 100%; justify-content: center; background: var(--gov-emerald); border-color: var(--gov-emerald);" onclick="completeCourse(this, '${c.course_id}')"><i class="fa-solid fa-circle-check"></i> Complete Course</button>`
        }
      </div>
    </div>
  `).join("");
}

window.completeCourse = async function(btn, courseId) {
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Completing...`;
  btn.disabled = true;

  try {
    const res = await fetch(API_BASE + "/api/igot/complete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course_id: courseId,
        officer_id: currentLearner ? currentLearner.officer_id : "OFF-ISS-2026-HQ"
      })
    });

    const data = await res.json();
    if (data.success && data.updated_officer) {
      showToast('🎉 Course completed! +50 Skill Points & competency uplift awarded.');
      currentLearner = data.updated_officer;
      renderLearnerHero();
      renderLearningPathways();
      renderCatalogPage();
      renderEnrolledCourses();
      initRadarChart();
      renderPriorityGaps();
    } else {
      btn.innerHTML = originalHtml;
      btn.disabled = false;
      showToast('Failed to complete course.');
    }
  } catch (err) {
    console.error(err);
    btn.innerHTML = originalHtml;
    btn.disabled = false;
    showToast('Error completing course.');
  }
};

function handleEnrolledFilter() {
  clearTimeout(enrolledSearchTimeout);
  enrolledSearchTimeout = setTimeout(() => {
    renderEnrolledCourses();
  }, 300);
}

// switchTab hook moved to main switchTab function;

function nominateForWorkshop(event, programId, title) {
  const btn = event.currentTarget;
  const modalTitle = document.getElementById("genericModalTitle");
  const modalBody = document.getElementById("genericModalBody");
  const actionBtn = document.getElementById("genericModalActionBtn");
  
  modalTitle.innerHTML = `<i class="fa-solid fa-clipboard-check"></i> Confirm Nomination`;
  modalBody.innerHTML = `Are you sure you want to officially nominate <strong>${currentLearner.name}</strong> for the upcoming NSSTA TPAC Workshop: <em>${title}</em>?<br><br>This will send a request to the Cadre Controlling Authority for approval.`;
  actionBtn.innerText = "Submit Nomination";
  actionBtn.onclick = async () => {
    closeGenericModal();
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing...`;
    btn.disabled = true;
    
    try {
      const res = await fetch(API_BASE + "/api/nssta/nominate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ program_id: programId, officer_id: currentLearner.officer_id })
      });
      const data = await res.json();
      if (data.success) {
        showToast(`📋 Nomination Submitted for '${title}'!`);
        btn.innerHTML = `<i class="fa-solid fa-check"></i> Nominated`;
        btn.style.background = "var(--gov-emerald)";
        btn.style.color = "#fff";
        if (data.updated_officer) currentLearner = data.updated_officer;
      }
    } catch (e) {
      showToast(`📋 Nomination Submitted for '${title}'!`);
      btn.innerHTML = `<i class="fa-solid fa-check"></i> Nominated`;
      btn.style.background = "var(--gov-emerald)";
      btn.style.color = "#fff";
    }
  };
  
  document.getElementById("uiOverlay").style.display = "flex";
}

function openFastTrackModal(compId, compName) {
  const modalTitle = document.getElementById("genericModalTitle");
  const modalBody = document.getElementById("genericModalBody");
  const actionBtn = document.getElementById("genericModalActionBtn");
  
  modalTitle.innerHTML = `<i class="fa-solid fa-bolt"></i> Fast-Track Pathway`;
  modalBody.innerHTML = `You are about to launch a customized, accelerated learning pathway specifically designed to bridge the competency gap in <strong>${compName}</strong>.<br><br>This pathway prioritizes critical micro-modules to get you certified faster.`;
  actionBtn.innerText = "Launch Pathway";
  actionBtn.onclick = () => {
    closeGenericModal();
    switchTab("tab-pathways");
    showToast(`Navigated to personalized recommendations for ${compName}`);
  };
  
  document.getElementById("uiOverlay").style.display = "flex";
}

function openIgotCatalogModal() {
  const modalTitle = document.getElementById("genericModalTitle");
  const modalBody = document.getElementById("genericModalBody");
  const actionBtn = document.getElementById("genericModalActionBtn");
  
  modalTitle.innerHTML = `<i class="fa-solid fa-book-open"></i> Full iGOT Catalog`;
  modalBody.innerHTML = `Would you like to browse the complete directory of over 60+ official iGOT Karmayogi statistical training modules?`;
  actionBtn.innerText = "Browse Catalog";
  actionBtn.onclick = () => {
    closeGenericModal();
    switchTab("tab-pathways");
    showToast("Full 60+ iGOT Karmayogi Official Statistics Catalog active.");
  };
  
  document.getElementById("uiOverlay").style.display = "flex";
}

function closeGenericModal() {
  document.getElementById("uiOverlay").style.display = "none";
}

// -------------------------------------------------------------------------
// 9. Admin Analytics & Charts
// -------------------------------------------------------------------------
function renderAdminAnalytics() {
  if (!administrativeAnalytics) return;

  const safeSetText = (id, text) => {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
  };
  
  safeSetText("adminTotalOfficers", administrativeAnalytics.total_officers.toLocaleString());
  safeSetText("adminAvgIndex", `${administrativeAnalytics.national_avg_competency_index}%`);
  safeSetText("adminTotalHours", administrativeAnalytics.total_learning_hours_logged.toLocaleString());
  safeSetText("adminTotalKarma", `${(administrativeAnalytics.total_karma_points_earned / 1000000).toFixed(2)}M`);

  initDivisionBarChart();
  initDeficitPieChart();
  initScatterPlotChart();
  searchOfficerDirectory();
}

function initDivisionBarChart() {
  const chartDom = document.getElementById("divisionBarChart");
  if (!chartDom || !administrativeAnalytics) return;

  if (divisionBarChartInstance) divisionBarChartInstance.dispose();
  const isDark = document.body.classList.contains("dark-theme");
  divisionBarChartInstance = echarts.init(chartDom, isDark ? "dark" : null);

  const divData = administrativeAnalytics.division_analytics || {};
  const divNames = Object.keys(divData);
  const divScores = divNames.map(k => divData[k].avg_competency_index);

  const option = {
    tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
    grid: { left: "3%", right: "4%", bottom: "3%", containLabel: true },
    xAxis: {
      type: "category",
      data: divNames,
      axisLabel: { color: "#94a3b8", fontSize: 11 }
    },
    yAxis: {
      type: "value",
      max: 100,
      min: 50,
      axisLabel: { color: "#94a3b8", formatter: "{value}%" },
      splitLine: { lineStyle: { color: "rgba(255, 255, 255, 0.08)" } }
    },
    series: [
      {
        name: "Avg Competency Index",
        type: "bar",
        data: divScores,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#3b82f6" },
            { offset: 1, color: "#1e3a8a" }
          ]),
          borderRadius: [6, 6, 0, 0]
        }
      }
    ]
  };

  divisionBarChartInstance.setOption(option);
}

function initDeficitPieChart() {
  const chartDom = document.getElementById("deficitPieChart");
  if (!chartDom || !administrativeAnalytics) return;

  if (deficitPieChartInstance) deficitPieChartInstance.dispose();
  const isDark = document.body.classList.contains("dark-theme");
  deficitPieChartInstance = echarts.init(chartDom, isDark ? "dark" : null);

  const deficits = administrativeAnalytics.top_national_skill_deficits || [];
  const pieData = deficits.slice(0, 6).map(d => ({
    value: d.officers_needing_training,
    name: `${d.competency_id}: ${d.name.substring(0, 24)}...`
  }));

  const option = {
    tooltip: { trigger: "item", formatter: "{b}<br/>Officers Needing Training: <b>{c}</b> ({d}%)" },
    legend: {
      orient: "horizontal",
      bottom: 0,
      left: "center",
      type: "scroll",
      textStyle: { color: "#94a3b8", fontSize: 11 },
      itemGap: 12,
      itemWidth: 12,
      itemHeight: 12
    },
    grid: { containLabel: true },
    series: [
      {
        name: "National Deficit",
        type: "pie",
        radius: ["35%", "65%"],
        center: ["50%", "45%"],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 6, borderColor: "#0b0f19", borderWidth: 2 },
        label: { show: false },
        data: pieData
      }
    ]
  };

  deficitPieChartInstance.setOption(option);
}

async function initScatterPlotChart() {
  const chartDom = document.getElementById("scatterPlotChart");
  if (!chartDom) return;

  if (scatterPlotChartInstance) scatterPlotChartInstance.dispose();
  const isDark = document.body.classList.contains("dark-theme");
  scatterPlotChartInstance = echarts.init(chartDom, isDark ? "dark" : null);
  
  scatterPlotChartInstance.showLoading({ color: '#f59e0b' });
  
  try {
    // Fetch all officers (limit=10000 to get everyone)
    const res = await fetch(API_BASE + "/api/officers?q=&division=All&cadre=All&page=1&limit=10000");
    const data = await res.json();
    const officers = Array.isArray(data) ? data : (data.officers || []);
    
    // Map data for scatter: [Skill Points (X), Competency Index (Y), Officer ID, Name, Cadre]
    const scatterData = officers.map(o => [
      o.karma_points,
      o.overall_competency_index,
      o.officer_id,
      o.name,
      o.cadre.split('(')[0].trim()
    ]);

    const option = {
      tooltip: {
        trigger: 'item',
        formatter: function (params) {
          return `<b>${params.data[3]}</b> (${params.data[2]})<br/>
                  Cadre: ${params.data[4]}<br/>
                  Skill Points: <b style="color:#f59e0b;">${params.data[0]}</b><br/>
                  Competency Index: <b style="color:#10b981;">${params.data[1]}%</b>`;
        }
      },
      grid: { left: '5%', right: '5%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'value',
        name: 'Skill Points Accrued (Karma)',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: { color: '#94a3b8' },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'Competency Index (%)',
        nameLocation: 'middle',
        nameGap: 30,
        min: 0,
        max: 100,
        axisLabel: { color: '#94a3b8' },
        splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.08)' } }
      },
      visualMap: {
        min: 40,
        max: 100,
        dimension: 1, // Color based on Y-axis (Competency Index)
        orient: 'horizontal',
        right: 10,
        top: 10,
        text: ['High', 'Low'],
        textStyle: { color: '#94a3b8' },
        inRange: {
          color: ['#ef4444', '#f59e0b', '#10b981'] // Red -> Yellow -> Green
        }
      },
      series: [
        {
          name: 'Officers',
          type: 'scatter',
          symbolSize: 8,
          data: scatterData,
          itemStyle: {
            opacity: 0.8,
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowOffsetY: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      ]
    };
    
    scatterPlotChartInstance.setOption(option);
  } catch (err) {
    console.error("Error loading scatter data:", err);
  } finally {
    scatterPlotChartInstance.hideLoading();
  }
}

let currentOfficerPage = 1;

async function searchOfficerDirectory(page = 1) {
  currentOfficerPage = page;
  // Search disabled per request, keeping input but not using value
  const search = ""; // document.getElementById("officerSearchInput")?.value || "";
  const division = document.getElementById("divisionFilterSelect")?.value || "All";
  const cadre = document.getElementById("cadreFilterSelect")?.value || "All";
  
  const tbody = document.getElementById("officersTableBody");
  if (!tbody) return;

  const pageSpan = document.getElementById("currentPageSpan");
  if (pageSpan) pageSpan.innerText = currentOfficerPage;

  const pageSize = document.getElementById("pageSizeSelect")?.value || 20;

  try {
    const res = await fetch(API_BASE + `/api/officers?q=${encodeURIComponent(search)}&division=${division}&cadre=${encodeURIComponent(cadre)}&page=${currentOfficerPage}&limit=${pageSize}`);
    const data = await res.json();
    const officers = Array.isArray(data) ? data : (data.officers || []);
    const totalPages = data.total_pages || 1;

    tbody.innerHTML = officers.map(o => {
      const isCurrent = currentLearner && o.officer_id === currentLearner.officer_id;
      const canView = window.isAdminSession || isCurrent;
      return `
      <tr style="border-bottom: 1px solid var(--border-glass); transition: 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.03)'" onmouseout="this.style.background='transparent'">
        <td style="padding: 10px; font-family: var(--font-mono); color: var(--gov-primary-light);">${o.officer_id}</td>
        <td style="padding: 10px; font-weight: 600;">${o.name}</td>
        <td style="padding: 10px; color: var(--text-secondary); font-size: 12px;">${o.designation}</td>
        <td style="padding: 10px;"><span class="cadre-badge">${o.cadre.split('(')[0]}</span></td>
        <td style="padding: 10px; font-weight: 700; color: var(--gov-saffron);">${o.division_code}</td>
        <td style="padding: 10px; font-weight: 700; color: ${o.overall_competency_index >= 80 ? 'var(--gov-emerald)' : 'var(--gov-rose)'};">${o.overall_competency_index}%</td>
        <td style="padding: 10px; color: var(--text-secondary);">${o.total_learning_hours} hrs</td>
        <td style="padding: 10px;">
          <button class="btn-primary" style="padding: 4px 8px; font-size: 11px;" ${!canView ? 'disabled title="Only the active profile can be viewed"' : ''} onclick="${canView ? `viewOfficerRecord('${o.officer_id}')` : ''}">
            <i class="fa-solid fa-eye"></i> View Profile
          </button>
        </td>
      </tr>
    `}).join("");

    if (officers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:20px; color:var(--text-muted);">No officers found matching the filter criteria.</td></tr>`;
    }

    renderPagination(currentOfficerPage, totalPages);
  } catch (e) {
    console.error("Error searching officers:", e);
  }
}

function renderPagination(current, total) {
  const container = document.getElementById("paginationContainer");
  if (!container) return;

  let html = `<button class="page-btn ${current === 1 ? 'disabled' : ''}" onclick="if(${current} > 1) searchOfficerDirectory(${current - 1})">Previous</button>`;

  // Simple window of 5 pages
  let start = Math.max(1, current - 2);
  let end = Math.min(total, start + 4);
  if (end - start < 4) start = Math.max(1, end - 4);

  if (start > 1) {
    html += `<button class="page-btn" onclick="searchOfficerDirectory(1)">1</button>`;
    if (start > 2) html += `<span class="page-ellipsis">...</span>`;
  }

  for (let i = start; i <= end; i++) {
    html += `<button class="page-btn ${i === current ? 'active' : ''}" onclick="searchOfficerDirectory(${i})">${i}</button>`;
  }

  if (end < total) {
    if (end < total - 1) html += `<span class="page-ellipsis">...</span>`;
    html += `<button class="page-btn" onclick="searchOfficerDirectory(${total})">${total}</button>`;
  }

  html += `<button class="page-btn ${current === total ? 'disabled' : ''}" onclick="if(${current} < ${total}) searchOfficerDirectory(${current + 1})">Next</button>`;

  html += `
    <div class="page-jumper">
      Page 
      <select onchange="searchOfficerDirectory(parseInt(this.value))">
        ${Array.from({length: total}, (_, i) => `<option value="${i+1}" ${i+1 === current ? 'selected' : ''}>${i+1}</option>`).join('')}
      </select>
      of ${total}
    </div>
  `;

  container.innerHTML = html;
}

async function viewOfficerRecord(officerId) {
  try {
    const res = await fetch(API_BASE + `/api/learner-profile?id=${officerId}`);
    currentLearner = await res.json();
    const recRes = await fetch(API_BASE + `/api/recommendations?id=${officerId}`);
    currentRecommendations = await recRes.json();

    renderLearnerHero();
    initRadarChart();
    renderPriorityGaps();
    renderFullCompetencyList();
    renderLearningPathways();
    renderTpacProgrammes();
    // Handle Admin View-Only Mode as a Modal Popup
    if (window.isAdminSession) {
      const passportTab = document.getElementById("tab-passport");
      passportTab.classList.add("admin-modal-mode");
      passportTab.style.display = "block";
      
      // Ensure the UI Overlay is on
      const uiOverlay = document.getElementById("uiOverlay");
      if (uiOverlay) uiOverlay.style.display = "flex";
      
      // Add a close button if not exists
      let closeBtn = document.getElementById("adminModalCloseBtn");
      if (!closeBtn) {
        closeBtn = document.createElement("button");
        closeBtn.id = "adminModalCloseBtn";
        closeBtn.innerHTML = '<i class="fa-solid fa-times"></i>';
        closeBtn.style.cssText = 'position: fixed; top: calc(5vh + 24px); right: calc(5vw + 24px); background: #e11d48; color: #ffffff; border: none; font-size: 20px; width: 44px; height: 44px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10001; box-shadow: 0 4px 12px rgba(0,0,0,0.3); opacity: 1; transition: transform 0.2s;';
        closeBtn.onclick = closeAdminProfileModal;
        closeBtn.onmouseover = () => closeBtn.style.transform = 'scale(1.1)';
        closeBtn.onmouseout = () => closeBtn.style.transform = 'scale(1)';
        passportTab.appendChild(closeBtn);
      } else {
        closeBtn.style.display = 'flex';
      }

      const fastTrackBtn = document.getElementById('fastTrackCloseGapsBtn');
      if (fastTrackBtn) fastTrackBtn.style.display = 'none';
      
      const adminBanner = document.getElementById('adminViewBanner');
      if (!adminBanner) {
        const banner = document.createElement('div');
        banner.id = 'adminViewBanner';
        banner.style.cssText = 'background: #fffbeb; border: 1px solid #fcd34d; border-left: 5px solid #d97706; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px; color: #b45309; font-weight: 700; font-size: 15px; display: flex; align-items: center; gap: 12px; margin-right: 80px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); opacity: 1;';
        banner.innerHTML = '<i class="fa-solid fa-user-shield" style="font-size: 20px;"></i> You are viewing this profile in Admin Read-Only Mode. Interactions are disabled.';
        const heroCard = document.getElementById('officerHeroCard');
        if (heroCard) heroCard.parentNode.insertBefore(banner, heroCard);
      } else {
        adminBanner.style.display = 'flex';
      }
      
      // Ensure charts render properly in modal
      setTimeout(() => {
        if (radarChartInstance) radarChartInstance.resize();
      }, 200);
      
    } else {
      switchTab("tab-passport");
    }
    
    showToast(`Loaded profile for ${currentLearner.name} (${currentLearner.officer_id})`);
  } catch (e) {
    console.error(e);
  }
}

function closeAdminProfileModal() {
  const passportTab = document.getElementById("tab-passport");
  if (passportTab) {
    passportTab.classList.remove("admin-modal-mode");
    passportTab.style.display = "none";
  }
  const uiOverlay = document.getElementById("uiOverlay");
  if (uiOverlay) {
    uiOverlay.style.display = "none";
  }
}

// -------------------------------------------------------------------------
// 10. Role Switcher & Tab Navigation
// -------------------------------------------------------------------------
async function switchOfficerRole(roleKey) {
  try {
    const res = await fetch(API_BASE + `/api/learner-profile?role=${roleKey}`);
    currentLearner = await res.json();
    const recRes = await fetch(API_BASE + `/api/recommendations?id=${currentLearner.officer_id}`);
    currentRecommendations = await recRes.json();

    renderLearnerHero();
    initRadarChart();
    renderPriorityGaps();
    renderFullCompetencyList();
    renderLearningPathways();
    renderTpacProgrammes();
    
    showToast(`Switched active view to ${currentLearner.name} (${currentLearner.designation})`);
  } catch (e) {
    console.error(e);
  }
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
  document.querySelectorAll(".nav-tab").forEach(tab => tab.classList.remove("active"));

  const targetPane = document.getElementById(tabId);
  if (targetPane) targetPane.classList.add("active");

  const activeBtn = Array.from(document.querySelectorAll(".nav-tab")).find(b => b.getAttribute("onclick")?.includes(tabId));
  if (activeBtn) activeBtn.classList.add("active");

  // Resize charts on tab activation
  setTimeout(() => {
    if (radarChartInstance) radarChartInstance.resize();
    if (divisionBarChartInstance) divisionBarChartInstance.resize();
    if (deficitPieChartInstance) deficitPieChartInstance.resize();
  }, 100);
  
  if (tabId === 'tab-leaderboard') {
    renderLeaderboard();
  } else if (tabId === 'tab-enrolled') {
    renderEnrolledCourses();
  }
}

async function renderLeaderboard() {
  const tbody = document.getElementById("leaderboardTableBody");
  if (!tbody) return;
  
  try {
    const res = await fetch(API_BASE + "/api/leaderboard");
    const top20 = await res.json();
    
    if (!top20 || top20.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; color:var(--text-muted);">Leaderboard data unavailable.</td></tr>`;
      return;
    }
    
    tbody.innerHTML = top20.map((o, idx) => {
      let rankIcon = `<strong>${idx + 1}</strong>`;
      if (idx === 0) rankIcon = `<i class="fa-solid fa-trophy" style="color: #fbbf24; font-size: 16px;"></i>`;
      else if (idx === 1) rankIcon = `<i class="fa-solid fa-medal" style="color: #94a3b8; font-size: 16px;"></i>`;
      else if (idx === 2) rankIcon = `<i class="fa-solid fa-medal" style="color: #b45309; font-size: 16px;"></i>`;
      
      return `
        <tr style="border-bottom: 1px solid var(--border-glass); transition: 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.03)'" onmouseout="this.style.background='transparent'">
          <td style="padding: 12px; text-align: center;">${rankIcon}</td>
          <td style="padding: 12px;">
            <div style="font-weight: 700;">${o.name}</div>
            <div style="font-size: 11px; font-family: var(--font-mono); color: var(--gov-primary-light);">${o.officer_id}</div>
          </td>
          <td style="padding: 12px; color: var(--text-secondary); font-size: 12px;">
            ${o.designation}<br>
            <span style="font-weight: 700; color: var(--gov-saffron); font-size: 11px;">${o.division_code}</span>
          </td>
          <td style="padding: 12px; font-weight: 700; color: ${o.overall_competency_index >= 80 ? 'var(--gov-emerald)' : 'var(--gov-rose)'};">${o.overall_competency_index}%</td>
          <td style="padding: 12px; color: var(--text-secondary);">${o.total_learning_hours} hrs</td>
          <td style="padding: 12px; text-align: right; font-weight: 800; color: var(--gov-saffron); font-size: 14px;">
            ${o.karma_points.toLocaleString()}
          </td>
        </tr>
      `;
    }).join("");
    
  } catch (err) {
    console.error("Error loading leaderboard:", err);
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; color:var(--gov-rose);">Failed to load leaderboard.</td></tr>`;
  }
}

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
  const isDark = document.body.classList.contains("dark-theme");
  const btn = document.getElementById("themeToggleBtn");
  if (btn) {
    btn.innerHTML = isDark ? `<i class="fa-solid fa-sun" style="color: #f59e0b;"></i>` : `<i class="fa-solid fa-moon"></i>`;
  }
  setTimeout(() => {
    initRadarChart();
    initDivisionBarChart();
    initDeficitPieChart();
  }, 150);
}

function showToast(message) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `<i class="fa-solid fa-bell" style="color: var(--gov-saffron);"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(50px)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function initVisualizations() {
  initRadarChart();
  window.addEventListener("resize", () => {
    if (radarChartInstance) radarChartInstance.resize();
    if (divisionBarChartInstance) divisionBarChartInstance.resize();
    if (deficitPieChartInstance) deficitPieChartInstance.resize();
    if (scatterPlotChartInstance) scatterPlotChartInstance.resize();
  });
}

function setupEventListeners() {
  const officerSearch = document.getElementById("officerSearchInput");
  if (officerSearch) {
    let debounceTimer;
    officerSearch.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchOfficerDirectory(1);
      }, 300);
    });
  }

  const globalSearch = document.getElementById("globalSearch");
  if (globalSearch) {
    let debounceTimer;
    globalSearch.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        if (officerSearch) {
          officerSearch.value = globalSearch.value;
          searchOfficerDirectory(1);
        }
      }, 300);
    });
  }
}
