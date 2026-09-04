/**
 * AI Karmayogi Statistical Learning Assistant
 * Conversational RAG assistant answering official statistics questions,
 * diagnosing competency gaps, and providing course guidance.
 */

const API_BASE = (window.location.protocol === 'file:' || window.location.hostname === 'localhost' && window.location.port !== '8050') 
  ? 'http://localhost:8050' 
  : '';

function toggleAssistantModal() {
  const modal = document.getElementById("assistantModal");
  if (!modal) return;
  const isVisible = modal.style.display === "flex";
  modal.style.display = isVisible ? "none" : "flex";
  if (!isVisible) {
    document.getElementById("assistantInput")?.focus();
  }
}

function sendAssistantPrompt(promptText) {
  const input = document.getElementById("assistantInput");
  if (input) input.value = promptText;
  sendAssistantMessage();
}

async function sendAssistantMessage() {
  const input = document.getElementById("assistantInput");
  const msgContainer = document.getElementById("chatMessages");
  if (!input || !msgContainer) return;

  const query = input.value.trim();
  if (!query) return;

  // Add User Message
  const userDiv = document.createElement("div");
  userDiv.className = "chat-msg user";
  userDiv.innerText = query;
  msgContainer.appendChild(userDiv);
  input.value = "";
  msgContainer.scrollTop = msgContainer.scrollHeight;

  // Add Typing Indicator
  const typingDiv = document.createElement("div");
  typingDiv.className = "chat-msg bot";
  typingDiv.innerHTML = `<i class="fa-solid fa-spinner fa-spin" style="color: var(--gov-saffron);"></i> <em>Analyzing official statistical standards...</em>`;
  msgContainer.appendChild(typingDiv);
  msgContainer.scrollTop = msgContainer.scrollHeight;

  try {
    const res = await fetch(API_BASE + "/api/assistant/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        officer_id: (typeof currentLearner !== 'undefined' && currentLearner) ? currentLearner.officer_id : "OFF-ISS-2026-HQ"
      })
    });

    const data = await res.json();
    typingDiv.remove();

    const botDiv = document.createElement("div");
    botDiv.className = "chat-msg bot";
    
    // Markdown-like bold replacement
    let formattedText = data.answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    let actionsHtml = "";
    if (data.suggested_actions && data.suggested_actions.length > 0) {
      actionsHtml = `
        <div style="margin-top: 8px; display: flex; flex-wrap: wrap; gap: 4px;">
          ${data.suggested_actions.map(act => `
            <button class="tag-pill" style="cursor: pointer; background: rgba(59, 130, 246, 0.2); color: var(--gov-primary-light);" onclick="sendAssistantPrompt('${act}')">
              <i class="fa-solid fa-arrow-right"></i> ${act}
            </button>
          `).join("")}
        </div>
      `;
    }

    botDiv.innerHTML = `<div>${formattedText}</div>${actionsHtml}`;
    msgContainer.appendChild(botDiv);
    msgContainer.scrollTop = msgContainer.scrollHeight;
  } catch (e) {
    typingDiv.innerHTML = "I am ready to assist you with official statistical methodologies (SNA 2008, CPI, PLFS) and iGOT Karmayogi learning paths.";
  }
}
