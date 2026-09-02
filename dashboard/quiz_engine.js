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

document.addEventListener("DOMContentLoaded", async () => {
  await loadMaterials();
  // Pre-fill text with first material
  loadPreloadedMaterial("MAT-SNA-01");
});

async function loadMaterials() {
  try {
    const res = await fetch("/api/materials").catch(() => fetch("data/learning_materials.json"));
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

  if (!textContent.trim()) {
    showToast("⚠️ Please select a document or paste text content.");
    return;
  }

  showToast("🧠 AI NLP Engine parsing statistical concepts & generating MCQs...");

  try {
    const res = await fetch("/api/assessments/generate", {
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
    }
  } catch (e) {
    console.error(e);
    showToast("Generated AI Assessment from local knowledge base.");
    loadPresetAssessment();
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
        <span class="tag-pill"><i class="fa-solid fa-award"></i> +${q.karma_reward || 25} Karma</span>
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
    const res = await fetch("/api/assessments/submit", {
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
          ${q.is_correct ? `<i class="fa-solid fa-check"></i> Correct (+${q.karma_earned} Karma)` : `<i class="fa-solid fa-xmark"></i> Incorrect`}
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
