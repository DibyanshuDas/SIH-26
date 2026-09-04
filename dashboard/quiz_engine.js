/**
 * AI Assessment & MCQ Generation / Evaluation Engine (Interactive Quiz Arena)
 * Ingests documents/manuals, generates MCQs, runs timed tests, provides pedagogical explanations,
 * and dynamically updates official competency scores.
 */

let activeAssessment = null;
let currentQuestionIndex = 0;
let userAnswers = {};
let quizTimerInterval = null;
let timeRemainingSeconds = 900;
let quizStartTime = null;
let allMaterials = {};

// Handle local file:/// loading by pointing to the localhost server
const API_BASE = (window.location.protocol === 'file:' || window.location.hostname === 'localhost' && window.location.port !== '8050') 
  ? 'http://localhost:8050' 
  : '';

document.addEventListener("DOMContentLoaded", async () => {
  await loadMaterials();
  // Pre-fill text with first material
  loadPreloadedMaterial("MAT-SNA-01");
});

async function loadMaterials() {
  try {
    const res = await fetch(API_BASE + "/api/materials").catch(() => fetch("data/learning_materials.json"));
    allMaterials = await res.json();
  } catch (e) {
    console.error("Error loading learning materials:", e);
  }
}

function loadPreloadedMaterial(materialId) {
  const mat = allMaterials[materialId];
  if (!mat) return;

  const textArea = document.getElementById("materialTextContent");
  const targetComp = document.getElementById("targetCompSelect");

  if (textArea) textArea.value = mat.content.trim();
  if (targetComp && mat.target_competency) targetComp.value = mat.target_competency;
}

// -------------------------------------------------------------------------
// 1. AI Quiz Generation from Text
// -------------------------------------------------------------------------
async function generateAIQuiz() {
  const textContent = document.getElementById("materialTextContent")?.value || "";
  const targetComp = document.getElementById("targetCompSelect")?.value || "STAT-01";
  const numQuestions = parseInt(document.getElementById("questionCountSelect")?.value || "5");
  const docSelect = document.getElementById("preloadedDocSelect");
  const docTitle = docSelect ? docSelect.options[docSelect.selectedIndex].text : "Custom Guideline";
  
  // Find the button to add loading state
  const btn = document.querySelector('button[onclick="generateAIQuiz()"]');
  const originalBtnHTML = btn ? btn.innerHTML : "AI Generate Assessment";

  if (!textContent.trim()) {
    showToast("⚠️ Please select a document or paste text content.");
    return;
  }

  showToast("🧠 AI NLP Engine parsing statistical concepts & generating MCQs...");
  
  if (btn) {
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Generating...`;
    btn.disabled = true;
    btn.style.opacity = "0.7";
    btn.style.cursor = "not-allowed";
  }

  try {
    const res = await fetch(API_BASE + "/api/assessments/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: docTitle,
        content: textContent,
        target_competency: targetComp,
        num_questions: numQuestions
      })
    });

    const data = await res.json();
    if (data.success && data.assessment) {
      startQuizArena(data.assessment);
      showToast("✨ AI Assessment synthesized with pedagogical explanations!");
    } else {
      throw new Error("Failed to generate assessment payload.");
    }
  } catch (e) {
    console.error(e);
    showToast("Server generation failed. Falling back to local knowledge base.");
    loadPresetAssessment();
  } finally {
    if (btn) {
      btn.innerHTML = originalBtnHTML;
      btn.disabled = false;
      btn.style.opacity = "1";
      btn.style.cursor = "pointer";
    }
  }
}

async function loadPresetAssessment() {
  const docId = document.getElementById("preloadedDocSelect")?.value || "MAT-SNA-01";
  
  try {
    const res = await fetch("/api/assessments").catch(() => fetch("data/assessment_bank.json"));
    const bank = await res.json();
    const asm = bank.find(a => a.material_id === docId) || bank[0];
    startQuizArena(asm);
  } catch (e) {
    console.error(e);
  }
}

// -------------------------------------------------------------------------
// 2. Start Quiz Arena & Timer
// -------------------------------------------------------------------------
function startQuizArena(assessment) {
  activeAssessment = assessment;
  currentQuestionIndex = 0;
  userAnswers = {};
  timeRemainingSeconds = (assessment.time_limit_minutes || 15) * 60;
  quizStartTime = Date.now();

  const arena = document.getElementById("quizArenaContainer");
  const results = document.getElementById("quizResultsCard");
  if (arena) arena.style.display = "block";
  if (results) results.style.display = "none";

  document.getElementById("quizTitle").innerText = assessment.title;
  document.getElementById("totalQuestionsNum").innerText = assessment.questions.length;

  startTimer();
  renderCurrentQuestion();
  arena.scrollIntoView({ behavior: "smooth" });
}

function startTimer() {
  if (quizTimerInterval) clearInterval(quizTimerInterval);

  updateTimerDisplay();
  quizTimerInterval = setInterval(() => {
    timeRemainingSeconds--;
    updateTimerDisplay();

    if (timeRemainingSeconds <= 0) {
      clearInterval(quizTimerInterval);
      showToast("⏰ Time is up! Submitting answers automatically.");
      submitAssessment();
    }
  }, 1000);
}

function updateTimerDisplay() {
  const display = document.getElementById("timerDisplay");
  if (!display) return;

  const mins = Math.floor(timeRemainingSeconds / 60);
  const secs = timeRemainingSeconds % 60;
  display.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// -------------------------------------------------------------------------
// 3. Question Rendering & Option Selection
// -------------------------------------------------------------------------
function renderCurrentQuestion() {
  if (!activeAssessment) return;

  const questions = activeAssessment.questions;
  const q = questions[currentQuestionIndex];
  const container = document.getElementById("questionContainer");
  if (!container) return;

  document.getElementById("currentQuestionNum").innerText = currentQuestionIndex + 1;
  const selectedAnswer = userAnswers[q.id];

  const letters = ["A", "B", "C", "D"];

  container.innerHTML = `
    <div class="question-block">
      <div style="display: flex; gap: 8px; margin-bottom: 8px;">
        <span class="tag-pill" style="color: var(--gov-saffron);"><i class="fa-solid fa-tag"></i> ${q.question_type} Question</span>
        <span class="tag-pill"><i class="fa-solid fa-award"></i> +${q.karma_reward || 25} Skill Pts</span>
        <span class="tag-pill"><i class="fa-solid fa-signal"></i> ${q.difficulty || 'Intermediate'}</span>
      </div>
      <div class="question-text">${q.question_text}</div>
      <div class="options-grid">
        ${q.options.map((opt, idx) => `
          <div class="option-item ${selectedAnswer === idx ? 'selected' : ''}" onclick="selectAnswer('${q.id}', ${idx})">
            <div class="option-letter">${letters[idx]}</div>
            <div style="font-size: 13.5px; flex: 1;">${opt}</div>
          </div>
        `).join("")}
      </div>
    </div>
  `;

  // Update navigation buttons
  const prevBtn = document.getElementById("prevQuestionBtn");
  const nextBtn = document.getElementById("nextQuestionBtn");
  const submitBtn = document.getElementById("submitQuizBtn");

  if (prevBtn) prevBtn.style.visibility = currentQuestionIndex === 0 ? "hidden" : "visible";
  if (currentQuestionIndex === questions.length - 1) {
    if (nextBtn) nextBtn.style.display = "none";
    if (submitBtn) submitBtn.style.display = "inline-flex";
  } else {
    if (nextBtn) nextBtn.style.display = "inline-flex";
    if (submitBtn) submitBtn.style.display = "none";
  }
}

function selectAnswer(questionId, optionIndex) {
  userAnswers[questionId] = optionIndex;
  renderCurrentQuestion();
}

function navigateQuestion(direction) {
  if (!activeAssessment) return;
  const newIdx = currentQuestionIndex + direction;
  if (newIdx >= 0 && newIdx < activeAssessment.questions.length) {
    currentQuestionIndex = newIdx;
    renderCurrentQuestion();
  }
}

// -------------------------------------------------------------------------
// 4. Submit & Evaluate
// -------------------------------------------------------------------------
async function submitAssessment() {
  if (!activeAssessment) return;
  if (quizTimerInterval) clearInterval(quizTimerInterval);

  const timeSpent = Math.round((Date.now() - quizStartTime) / 1000);

  try {
    const res = await fetch(API_BASE + "/api/assessments/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        assessment_id: activeAssessment.assessment_id,
        answers: userAnswers,
        time_spent_seconds: timeSpent,
        officer_id: currentLearner?.officer_id || "OFF-ISS-2026-HQ"
      })
    });

    const evalResult = await res.json();
    renderQuizResults(evalResult);
  } catch (e) {
    console.error("Error submitting assessment:", e);
  }
}

function renderQuizResults(result) {
  const arena = document.getElementById("quizArenaContainer");
  const resultsCard = document.getElementById("quizResultsCard");

  if (arena) arena.style.display = "none";
  if (resultsCard) resultsCard.style.display = "block";

  document.getElementById("resultScoreVal").innerText = `${result.score_percentage}%`;
  document.getElementById("resultScoreVal").style.color = result.passed ? "var(--gov-emerald)" : "var(--gov-rose)";
  document.getElementById("resultUpliftVal").innerText = `+${result.competency_level_uplift} Level`;
  document.getElementById("resultKarmaVal").innerText = `+${result.karma_points_awarded}`;

  document.getElementById("resultHeaderTitle").innerHTML = result.passed ? 
    `<i class="fa-solid fa-award" style="color: var(--gov-saffron);"></i> Assessment Passed! Official Certification Awarded` :
    `<i class="fa-solid fa-circle-xmark" style="color: #ef4444;"></i> Assessment Incomplete (Passing: 70%)`;
  
  document.getElementById("resultHeaderSubtitle").innerText = result.feedback_summary;

  const reviewList = document.getElementById("questionsReviewList");
  if (!reviewList) return;

  const letters = ["A", "B", "C", "D"];

  reviewList.innerHTML = result.detailed_questions_review.map((q, idx) => `
    <div style="background: var(--bg-glass); border: 1px solid ${q.is_correct ? 'rgba(5, 150, 105, 0.3)' : 'rgba(225, 29, 72, 0.3)'}; border-radius: var(--radius-md); padding: 18px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-weight: 700; font-size: 14px;">Question ${idx + 1}: ${q.question_type}</span>
        <span class="${q.is_correct ? 'badge-gap-none' : 'badge-gap-high'}">
          ${q.is_correct ? `<i class="fa-solid fa-check"></i> Correct (+${q.karma_earned} Skill Pts)` : `<i class="fa-solid fa-xmark"></i> Incorrect`}
        </span>
      </div>
      <p style="font-size: 14px; font-weight: 600; margin-bottom: 12px;">${q.question_text}</p>
      
      <div style="display: grid; gap: 6px; margin-bottom: 12px;">
        ${q.options.map((opt, optIdx) => `
          <div style="padding: 8px 12px; border-radius: 6px; font-size: 12.5px; display: flex; align-items: center; gap: 8px; background: ${optIdx === q.correct_answer_index ? 'rgba(5, 150, 105, 0.2)' : (optIdx === q.user_answer_index ? 'rgba(225, 29, 72, 0.2)' : 'rgba(255, 255, 255, 0.03)')}; border: 1px solid ${optIdx === q.correct_answer_index ? 'var(--gov-emerald)' : (optIdx === q.user_answer_index ? 'var(--gov-rose)' : 'transparent')}">
            <strong>${letters[optIdx]}.</strong> 
            <span style="flex: 1;">${opt}</span>
            ${optIdx === q.correct_answer_index ? '<span style="color: var(--gov-emerald); font-weight: 700; font-size: 11px;">(Correct Answer)</span>' : ''}
            ${optIdx === q.user_answer_index && !q.is_correct ? '<span style="color: var(--gov-rose); font-weight: 700; font-size: 11px;">(Your Answer)</span>' : ''}
          </div>
        `).join("")}
      </div>

      <div class="explanation-box">
        <div class="explanation-header"><i class="fa-solid fa-lightbulb"></i> Pedagogical Explanation & Official Reference:</div>
        <p>${q.explanation}</p>
        <div style="margin-top: 6px; font-size: 11.5px; color: var(--gov-saffron); font-weight: 600;">
          <i class="fa-solid fa-quote-left"></i> Source Citation: ${q.citation}
        </div>
      </div>
    </div>
  `).join("");

  resultsCard.scrollIntoView({ behavior: "smooth" });

  // Update learner data if passed
  if (result.passed) {
    loadInitialData();
  }
}

function resetQuiz() {
  document.getElementById("quizResultsCard").style.display = "none";
  document.getElementById("quizArenaContainer").style.display = "none";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// -------------------------------------------------------------------------
// 6. File Upload Handling (PDF, DOCX, PPTX, TXT)
// -------------------------------------------------------------------------
const ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".pptx", ".txt"];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

// Drag-and-drop support
document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("fileUploadZone");
  if (!dropZone) return;

  ["dragenter", "dragover"].forEach(evt => {
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("drag-over");
    });
  });

  ["dragleave", "drop"].forEach(evt => {
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("drag-over");
    });
  });

  dropZone.addEventListener("drop", e => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processUploadedFile(files[0]);
    }
  });
});

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  processUploadedFile(file);
}

function processUploadedFile(file) {
  const ext = "." + file.name.split(".").pop().toLowerCase();

  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    showToast("⚠️ Unsupported file type. Please upload PDF, DOCX, PPTX, or TXT files.");
    return;
  }

  if (file.size > MAX_FILE_SIZE) {
    showToast("⚠️ File too large. Maximum size is 10 MB.");
    return;
  }

  // Show uploaded file info
  const fileInfo = document.getElementById("uploadedFileInfo");
  const uploadZone = document.getElementById("fileUploadZone");
  const fileNameEl = document.getElementById("uploadedFileName");
  const fileSizeEl = document.getElementById("uploadedFileSize");
  const statusEl = document.getElementById("uploadStatus");

  if (uploadZone) uploadZone.style.display = "none";
  if (fileInfo) fileInfo.style.display = "flex";
  if (fileNameEl) fileNameEl.textContent = file.name;
  if (fileSizeEl) fileSizeEl.textContent = formatFileSize(file.size);
  if (statusEl) {
    statusEl.className = "upload-status-badge processing";
    statusEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
  }

  // Handle TXT files locally
  if (ext === ".txt") {
    const reader = new FileReader();
    reader.onload = (e) => {
      const textContent = e.target.result;
      const textArea = document.getElementById("materialTextContent");
      if (textArea) textArea.value = textContent;
      if (statusEl) {
        statusEl.className = "upload-status-badge success";
        statusEl.innerHTML = '<i class="fa-solid fa-circle-check"></i> Ready';
      }
      showToast("✅ Text file loaded successfully. Content ready for AI assessment generation.");
    };
    reader.onerror = () => {
      if (statusEl) {
        statusEl.className = "upload-status-badge error";
        statusEl.innerHTML = '<i class="fa-solid fa-circle-xmark"></i> Failed';
      }
      showToast("❌ Error reading text file.");
    };
    reader.readAsText(file);
    return;
  }

  // Upload binary files (PDF, DOCX, PPTX) to server for extraction
  const formData = new FormData();
  formData.append("file", file);

  fetch(API_BASE + "/api/assessments/upload-material", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.success && data.extracted_text) {
      const textArea = document.getElementById("materialTextContent");
      if (textArea) textArea.value = data.extracted_text;
      if (statusEl) {
        statusEl.className = "upload-status-badge success";
        statusEl.innerHTML = '<i class="fa-solid fa-circle-check"></i> Ready';
      }
      showToast(`✅ ${file.name} processed successfully. ${data.pages || ""} Content extracted and ready for AI assessment.`);
    } else {
      throw new Error(data.error || "Failed to extract text");
    }
  })
  .catch(err => {
    console.error("File upload error:", err);
    if (statusEl) {
      statusEl.className = "upload-status-badge error";
      statusEl.innerHTML = '<i class="fa-solid fa-circle-xmark"></i> Failed';
    }
    showToast(`❌ Error processing file: ${err.message}`);
  });
}

function clearUploadedFile() {
  const fileInfo = document.getElementById("uploadedFileInfo");
  const uploadZone = document.getElementById("fileUploadZone");
  const fileInput = document.getElementById("fileUploadInput");

  if (fileInfo) fileInfo.style.display = "none";
  if (uploadZone) uploadZone.style.display = "flex";
  if (fileInput) fileInput.value = "";
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
}
