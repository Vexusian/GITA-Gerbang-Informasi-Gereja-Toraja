/**
 * GITA - UI Renderer & DOM Controller
 * Universal Vanilla JS Module
 */

(function(window) {
  'use strict';

  window.GITA = window.GITA || {};

  function escapeHTML(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function formatDocumentMarkdown(text) {
    if (!text) return "";

    const escaped = escapeHTML(text);

    // Bold **text**
    let formatted = escaped.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Italic *text*
    formatted = formatted.replace(/\*(.*?)\*/g, "<em>$1</em>");

    // Pisahkan baris
    const lines = formatted.split("\n");
    const output = [];
    let inUl = false;
    let inOl = false;

    for (let line of lines) {
      line = line.trim();

      if (!line) {
        if (inUl) { output.push("</ul>"); inUl = false; }
        if (inOl) { output.push("</ol>"); inOl = false; }
        continue;
      }

      // Numbered list item: "1. text"
      const olMatch = line.match(/^(\d+)\.\s+(.*)/);
      if (olMatch) {
        if (inUl) { output.push("</ul>"); inUl = false; }
        if (!inOl) { output.push("<ol>"); inOl = true; }
        output.push(`<li>${olMatch[2]}</li>`);
        continue;
      }

      // Unordered list item: "* text" or "- text"
      const ulMatch = line.match(/^[\*\-]\s+(.*)/);
      if (ulMatch) {
        if (inOl) { output.push("</ol>"); inOl = false; }
        if (!inUl) { output.push("<ul>"); inUl = true; }
        output.push(`<li>${ulMatch[1]}</li>`);
        continue;
      }

      // Regular line
      if (inUl) { output.push("</ul>"); inUl = false; }
      if (inOl) { output.push("</ol>"); inOl = false; }

      output.push(`<p>${line}</p>`);
    }

    if (inUl) output.push("</ul>");
    if (inOl) output.push("</ol>");

    return output.join("");
  }

  const STATUS_CONFIG = {
    success: {
      label: "Terverifikasi Dokumen TGT",
      class: "success",
      icon: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`
    },
    not_found: {
      label: "Ketentuan Tidak Ditemukan",
      class: "warning",
      icon: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
    },
    insufficient_evidence: {
      label: "Informasi Tidak Lengkap",
      class: "warning",
      icon: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`
    },
    error: {
      label: "Kendala Pemrosesan",
      class: "error",
      icon: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`
    }
  };

  function appendUserMessage(container, text) {
    const turnEl = document.createElement("div");
    turnEl.className = "chat-turn";

    const userContainer = document.createElement("div");
    userContainer.className = "user-query-container";

    userContainer.innerHTML = `
      <div class="user-query-bubble">
        <div class="user-query-text">${escapeHTML(text)}</div>
      </div>
    `;

    turnEl.appendChild(userContainer);
    container.appendChild(turnEl);
    scrollToBottom();
  }

  function showLoadingIndicator(container) {
    const loadingEl = document.createElement("div");
    loadingEl.id = "active-loading-indicator";
    loadingEl.className = "chat-turn";

    loadingEl.innerHTML = `
      <div class="loading-turn">
        <div class="loading-header">
          <div class="loading-spinner-ring"></div>
          <span>Mencari pasal dan menelaah rujukan dokumen Tata Gereja Toraja...</span>
        </div>
        <div class="skeleton-line w-full"></div>
        <div class="skeleton-line w-80"></div>
        <div class="skeleton-line w-60"></div>
      </div>
    `;

    container.appendChild(loadingEl);
    scrollToBottom();
    return loadingEl;
  }

  function removeLoadingIndicator() {
    const loadingEl = document.getElementById("active-loading-indicator");
    if (loadingEl) {
      loadingEl.remove();
    }
  }

  function appendAssistantResponse(container, data) {
    removeLoadingIndicator();

    const turnEl = document.createElement("div");
    turnEl.className = "chat-turn";

    const statusInfo = STATUS_CONFIG[data.status] || STATUS_CONFIG.info;
    const formattedAnswer = formatDocumentMarkdown(data.answer);

    const cardEl = document.createElement("div");
    cardEl.className = "assistant-response-card";

    let html = `
      <div class="response-header">
        <div class="assistant-identity">
          <div class="assistant-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
          </div>
          <span class="assistant-name">GITA Assistant</span>
        </div>
        <div class="status-pill ${statusInfo.class}">
          ${statusInfo.icon}
          <span>${statusInfo.label}</span>
        </div>
      </div>

      <div class="response-body">
        ${formattedAnswer}
      </div>
    `;

    if (data.sources && data.sources.length > 0) {
      html += `
        <div class="source-section">
          <div class="source-header">
            <div class="source-title">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
              <span>Referensi Resmi Tata Gereja Toraja</span>
            </div>
            <span class="source-count-badge">${data.sources.length} Rujukan</span>
          </div>
          <div class="citation-cards-list">
      `;

      data.sources.forEach((source, index) => {
        const sectionName = escapeHTML(source.section || "Tata Gereja Toraja");
        const chapterName = source.chapter ? `BAB ${escapeHTML(source.chapter)}` : "";
        const articleName = source.article ? `Pasal ${escapeHTML(source.article)}` : "";
        const pageInfo = source.page_start ? `Halaman ${source.page_start}${source.page_end && source.page_end !== source.page_start ? '–' + source.page_end : ''}` : "";
        const excerpt = escapeHTML(source.content || "Teks pasal rujukan tercatat dalam dokumen.");
        const excerptId = `citation-excerpt-${Date.now()}-${index}`;

        html += `
          <div class="citation-card">
            <div class="citation-meta-row">
              <span class="citation-badge">${articleName || sectionName}</span>
              <span class="citation-doc-info">${chapterName ? chapterName + ' • ' : ''}${sectionName}</span>
              ${pageInfo ? `<span class="citation-page">(${pageInfo})</span>` : ''}
              <button type="button" class="citation-toggle-btn" data-target="${excerptId}">
                <span>Kutipan Pasal</span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
            </div>
            <div id="${excerptId}" class="citation-excerpt">
              ${excerpt}
            </div>
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;
    }

    cardEl.innerHTML = html;
    turnEl.appendChild(cardEl);
    container.appendChild(turnEl);

    // Expand/collapse listener
    cardEl.querySelectorAll(".citation-toggle-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-target");
        const excerptEl = document.getElementById(targetId);
        if (excerptEl) {
          const isExpanded = excerptEl.classList.toggle("expanded");
          btn.querySelector("span").textContent = isExpanded ? "Tutup Kutipan" : "Kutipan Pasal";
          btn.querySelector("svg").style.transform = isExpanded ? "rotate(180deg)" : "rotate(0deg)";
          if (isExpanded) {
            scrollToBottom(true);
          }
        }
      });
    });

    scrollToBottom();
  }

  function appendErrorMessage(container, errorMessage, onRetry) {
    removeLoadingIndicator();

    const turnEl = document.createElement("div");
    turnEl.className = "chat-turn";

    const errorBox = document.createElement("div");
    errorBox.className = "assistant-response-card";

    errorBox.innerHTML = `
      <div class="notice-box error">
        <div class="notice-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <div class="notice-content">
          <h4>Gagal Menghubungi Layanan</h4>
          <p>${escapeHTML(errorMessage)}</p>
          <button type="button" class="btn-retry" id="btn-retry-action">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1 4 1 10 7 10"></polyline>
              <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
            </svg>
            <span>Ulangi Pertanyaan</span>
          </button>
        </div>
      </div>
    `;

    turnEl.appendChild(errorBox);
    container.appendChild(turnEl);

    const retryBtn = errorBox.querySelector("#btn-retry-action");
    if (retryBtn && typeof onRetry === "function") {
      retryBtn.addEventListener("click", onRetry);
    }

    scrollToBottom();
  }

  function scrollToBottom(smooth = true) {
    requestAnimationFrame(() => {
      const scrollingElement = document.scrollingElement || document.documentElement;
      scrollingElement.scrollTo({
        top: scrollingElement.scrollHeight,
        behavior: smooth ? "smooth" : "auto"
      });
    });
  }

  window.GITA.UI = {
    escapeHTML,
    formatDocumentMarkdown,
    appendUserMessage,
    showLoadingIndicator,
    removeLoadingIndicator,
    appendAssistantResponse,
    appendErrorMessage,
    scrollToBottom
  };
})(typeof window !== 'undefined' ? window : this);
