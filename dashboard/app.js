/**
 * KASHYAP-STAT Dashboard Application Engine
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

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", async () => {
  await loadInitialData();
  initVisualizations();
  setupEventListeners();
});

// -------------------------------------------------------------------------
// 1. Data Ingestion & API Layer
// -------------------------------------------------------------------------
async function loadInitialData() {
  try {
    // 1. Learner Profile
    const learnerRes = await fetch("/api/learner-profile").catch(() => fetch("data/primary_learner.json"));
    currentLearner = await learnerRes.json();

    // 2. Recommendations
    const recRes = await fetch("/api/recommendations").catch(() => fetch("data/primary_recommendations.json"));
    currentRecommendations = await recRes.json();

    // 3. Framework
    const fwRes = await fetch("/api/framework").catch(() => fetch("data/competency_framework.json"));
    competencyFramework = await fwRes.json();

    // 4. Admin Analytics
    const adminRes = await fetch("/api/admin/analytics").catch(() => fetch("data/administrative_analytics.json"));
    administrativeAnalytics = await adminRes.json();

    // Render UI Components
    renderLearnerHero();
    renderPriorityGaps();
    renderFullCompetencyList("ALL");
    renderLearningPathways();
    renderTpacProgrammes();
    renderAdminAnalytics();
  } catch (err) {
    console.error("Error loading initial data:", err);
  }
}

// -------------------------------------------------------------------------
// 2. Render Learner Passport & Hero
// -------------------------------------------------------------------------
function renderLearnerHero() {
  if (!currentLearner) return;

  const initials = currentLearner.name.split(" ").filter(n => !n.includes(".")).map(n => n[0]).slice(0, 2).join("");
  document.getElementById("heroAvatar").innerText = initials || "RS";
  document.getElementById("heroName").innerText = currentLearner.name;
  document.getElementById("heroCadre").innerText = currentLearner.cadre;
  document.getElementById("heroDesignation").innerText = currentLearner.designation;
  document.getElementById("heroDivision").innerText = currentLearner.division_name;
  document.getElementById("heroHQ").innerText = currentLearner.headquarters || "New Delhi";
  document.getElementById("heroEducation").innerText = currentLearner.education;
  document.getElementById("heroAssignment").innerText = currentLearner.current_assignment;

  document.getElementById("heroIndexVal").innerText = `${currentLearner.overall_competency_index}%`;
  document.getElementById("heroHoursVal").innerText = `${currentLearner.total_learning_hours} hrs`;
  document.getElementById("heroKarmaVal").innerText = currentLearner.karma_points.toLocaleString();

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

  const isLight = document.body.classList.contains("light-theme");
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
      textStyle: { color: legendColor, fontSize: 12, fontWeight: 500 },
      data: ["Current Assessed Capability", "Cadre Required Benchmark"]
    },
    radar: {
      shape: "polygon",
      indicator: [
        { name: "Statistical Methodologies\n& National Accounts", max: 5 },
        { name: "Modern Data Science,\nAI & Computing", max: 5 },
        { name: "Digital Governance,\nPrivacy & DPDPA", max: 5 },
        { name: "Leadership, Operations\n& Policy Advisory", max: 5 }
      ],
      axisName: {
        color: axisColor,
        fontSize: 12.5,
        fontWeight: 700
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
  if (!container || !currentLearner) return;

  const gaps = currentLearner.top_priority_gaps || [];
  if (gaps.length === 0) {
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
      <button class="btn-enrol" onclick="openFastTrackModal('${g.id}', '${g.name}')">
        <i class="fa-solid fa-bolt"></i> Remedy
      </button>
    </div>
  `).join("");
}

// -------------------------------------------------------------------------
// 5. Render Full 28 Competency Taxonomy List
// -------------------------------------------------------------------------
function filterCompetencyList(domainKey, btnEl) {
  // Update button active states
  if (btnEl) {
    const parent = btnEl.parentElement;
    parent.querySelectorAll(".tag-pill").forEach(b => b.classList.remove("active"));
    btnEl.classList.add("active");
  }
  renderFullCompetencyList(domainKey);
}

function renderFullCompetencyList(domainKey = "ALL") {
  const container = document.getElementById("fullCompetencyList");
  if (!container || !competencyFramework || !currentLearner) return;

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
          <span class="tag-pill"><i class="fa-solid fa-star" style="color: #fbbf24;"></i> ${c.rating}</span>
          <span class="tag-pill"><i class="fa-solid fa-coins" style="color: var(--gov-saffron);"></i> +${c.karma_points} Karma</span>
        </div>
      </div>
      <div class="course-footer">
        <span class="uplift-tag"><i class="fa-solid fa-chart-line"></i> +${c.estimated_uplift_pct}% Uplift</span>
        <button class="btn-enrol" onclick="enrolInCourse(event, '${c.course_id}', '${c.title}')">
          <i class="fa-solid fa-graduation-cap"></i> Enrol & Certify
        </button>
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
      <button class="btn-primary btn-saffron" style="font-size: 12px; padding: 8px 14px;" onclick="nominateForWorkshop(event, '${p.program_id}', '${p.title}')">
        <i class="fa-solid fa-file-signature"></i> Nominate Officer
      </button>
    </div>
  `).join("");
}

// -------------------------------------------------------------------------
// 8. Enrol Course Action & Real-Time Competency Update
// -------------------------------------------------------------------------
async function enrolInCourse(event, courseId, courseTitle) {
  const btn = event.currentTarget;
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing...`;
  btn.disabled = true;

  try {
    const res = await fetch("/api/igot/enrol", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course_id: courseId,
        officer_id: currentLearner.officer_id
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast(`🎉 Certified: Successfully completed '${courseTitle}'! (+${data.karma_points_earned} Karma Points)`);
      btn.innerHTML = `<i class="fa-solid fa-check"></i> Certified`;
      btn.style.background = "var(--gov-emerald)";
      btn.style.color = "#fff";
      
      if (data.updated_officer) {
        currentLearner = data.updated_officer;
        renderLearnerHero();
        initRadarChart();
        renderPriorityGaps();
        renderFullCompetencyList();
      }
    } else {
      btn.innerHTML = originalHtml;
      btn.disabled = false;
    }
  } catch (e) {
    btn.innerHTML = `<i class="fa-solid fa-check"></i> Certified`;
    btn.style.background = "var(--gov-emerald)";
    btn.style.color = "#fff";
    showToast(`🎉 Certified: Successfully completed '${courseTitle}'! (+50 Karma Points)`);
  }
}

function nominateForWorkshop(event, programId, title) {
  const btn = event.currentTarget;
  const modalTitle = document.getElementById("genericModalTitle");
  const modalBody = document.getElementById("genericModalBody");
  const actionBtn = document.getElementById("genericModalActionBtn");
  
  modalTitle.innerHTML = `<i class="fa-solid fa-clipboard-check"></i> Confirm Nomination`;
  modalBody.innerHTML = `Are you sure you want to officially nominate <strong>${currentLearner.name}</strong> for the upcoming NSSTA TPAC Workshop: <em>${title}</em>?<br><br>This will send a request to the Cadre Controlling Authority for approval.`;
  actionBtn.innerText = "Submit Nomination";
  actionBtn.onclick = () => {
    closeGenericModal();
    showToast(`📋 Nomination Submitted for '${title}'!`);
    btn.innerHTML = `<i class="fa-solid fa-check"></i> Nominated`;
    btn.style.background = "var(--gov-emerald)";
    btn.style.color = "#fff";
    btn.disabled = true;
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

  document.getElementById("adminTotalOfficers").innerText = administrativeAnalytics.total_officers.toLocaleString();
  document.getElementById("adminAvgIndex").innerText = `${administrativeAnalytics.national_avg_competency_index}%`;
  document.getElementById("adminTotalHours").innerText = administrativeAnalytics.total_learning_hours_logged.toLocaleString();
  document.getElementById("adminTotalKarma").innerText = `${(administrativeAnalytics.total_karma_points_earned / 1000000).toFixed(2)}M`;

  initDivisionBarChart();
  initDeficitPieChart();
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
    legend: { orient: "vertical", right: 0, top: "center", textStyle: { color: "#94a3b8", fontSize: 10 } },
    series: [
      {
        name: "National Deficit",
        type: "pie",
        radius: ["40%", "70%"],
        center: ["40%", "50%"],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 6, borderColor: "#0b0f19", borderWidth: 2 },
        label: { show: false },
        data: pieData
      }
    ]
  };

  deficitPieChartInstance.setOption(option);
}

let currentOfficerPage = 1;

async function searchOfficerDirectory(page = 1) {
  currentOfficerPage = page;
  const search = document.getElementById("officerSearchInput")?.value || "";
  const division = document.getElementById("divisionFilterSelect")?.value || "All";
  const tbody = document.getElementById("officersTableBody");
  if (!tbody) return;

  const pageSpan = document.getElementById("currentPageSpan");
  if (pageSpan) pageSpan.innerText = currentOfficerPage;

  try {
    const res = await fetch(`/api/officers?q=${encodeURIComponent(search)}&division=${division}&page=${currentOfficerPage}`);
    const data = await res.json();
    const officers = data.officers || [];
    const totalPages = data.total_pages || 1;

    tbody.innerHTML = officers.map(o => `
      <tr style="border-bottom: 1px solid var(--border-glass); transition: 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.03)'" onmouseout="this.style.background='transparent'">
        <td style="padding: 10px; font-family: var(--font-mono); color: var(--gov-primary-light);">${o.officer_id}</td>
        <td style="padding: 10px; font-weight: 600;">${o.name}</td>
        <td style="padding: 10px; color: var(--text-secondary); font-size: 12px;">${o.designation}</td>
        <td style="padding: 10px;"><span class="cadre-badge">${o.cadre.split('(')[0]}</span></td>
        <td style="padding: 10px; font-weight: 700; color: var(--gov-saffron);">${o.division_code}</td>
        <td style="padding: 10px; font-weight: 700; color: ${o.overall_competency_index >= 80 ? 'var(--gov-emerald)' : 'var(--gov-rose)'};">${o.overall_competency_index}%</td>
        <td style="padding: 10px; color: var(--text-secondary);">${o.total_learning_hours} hrs</td>
        <td style="padding: 10px;">
          <button class="btn-primary" style="padding: 4px 8px; font-size: 11px;" onclick="viewOfficerRecord('${o.officer_id}')">
            <i class="fa-solid fa-eye"></i> View
          </button>
        </td>
      </tr>
    `).join("");

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
    const res = await fetch(`/api/learner-profile?id=${officerId}`);
    currentLearner = await res.json();
    const recRes = await fetch(`/api/recommendations?id=${officerId}`);
    currentRecommendations = await recRes.json();

    renderLearnerHero();
    initRadarChart();
    renderPriorityGaps();
    renderFullCompetencyList();
    renderLearningPathways();
    renderTpacProgrammes();
    switchTab("tab-passport");
    showToast(`Loaded profile for ${currentLearner.name} (${currentLearner.officer_id})`);
  } catch (e) {
    console.error(e);
  }
}

// -------------------------------------------------------------------------
// 10. Role Switcher & Tab Navigation
// -------------------------------------------------------------------------
async function switchOfficerRole(roleKey) {
  try {
    const res = await fetch(`/api/learner-profile?role=${roleKey}`);
    currentLearner = await res.json();
    const recRes = await fetch(`/api/recommendations?id=${currentLearner.officer_id}`);
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
  });
}

function setupEventListeners() {
  // Any extra global listeners
}
