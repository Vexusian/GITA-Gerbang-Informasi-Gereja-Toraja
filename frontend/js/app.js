/**
 * GITA - Main Application Controller
 * Universal Vanilla JS Module
 */

(function(window) {
  'use strict';

  document.addEventListener("DOMContentLoaded", () => {
    const GITA = window.GITA || {};
    const config = GITA.CONFIG || {};
    const ui = GITA.UI || {};
    const askQuestion = GITA.askQuestion;

    // DOM Elements
    const conversationContainer = document.getElementById("conversation-container");
    const emptyState = document.getElementById("empty-state");
    const queryForm = document.getElementById("query-form");
    const queryInput = document.getElementById("query-input");
    const btnSend = document.getElementById("btn-send");
    const btnNewChat = document.getElementById("btn-new-chat");
    const modeToggle = document.getElementById("mode-toggle");
    const modeLabel = document.getElementById("mode-label");
    const samplePromptCards = document.querySelectorAll(".sample-prompt-card");

    let isProcessing = false;
    let lastQuery = "";

    // 1. Sinkronisasi Dinamis Tinggi Composer ke CSS Variable (--composer-height)
    const inputDock = document.querySelector(".input-dock");
    if (inputDock) {
      const updateComposerHeight = () => {
        const height = Math.ceil(inputDock.getBoundingClientRect().height);
        if (height > 0) {
          document.documentElement.style.setProperty("--composer-height", `${height}px`);
        }
      };

      if (typeof ResizeObserver !== "undefined") {
        const ro = new ResizeObserver(updateComposerHeight);
        ro.observe(inputDock);
      }
      window.addEventListener("resize", updateComposerHeight, { passive: true });
      updateComposerHeight();
    }

    // 2. Inisialisasi Tampilan Mode (Simulasi TGT vs Live Backend)
    updateModeUI();

    if (modeToggle) {
      modeToggle.addEventListener("click", () => {
        config.USE_MOCK = !config.USE_MOCK;
        updateModeUI();
      });
    }

    function updateModeUI() {
      if (!modeLabel) return;
      if (config.USE_MOCK) {
        modeLabel.textContent = "Mode: Simulasi TGT";
        modeLabel.title = "Menggunakan data simulasi chunks.json (Klik untuk beralih ke Backend Live)";
        modeToggle.style.borderColor = "var(--border-subtle)";
        modeToggle.style.color = "var(--text-secondary)";
      } else {
        modeLabel.textContent = "Mode: Live Backend";
        modeLabel.title = `Menghubungi ${config.API_BASE_URL} (Klik untuk beralih ke Simulasi)`;
        modeToggle.style.borderColor = "var(--navy-primary)";
        modeToggle.style.color = "var(--navy-primary)";
      }
    }

    // 2. Textarea Auto-Resize Dinamis
    if (queryInput) {
      queryInput.addEventListener("input", () => {
        queryInput.style.height = "auto";
        const newHeight = Math.min(queryInput.scrollHeight, 160);
        queryInput.style.height = `${Math.max(48, newHeight)}px`;

        // Validasi tombol kirim
        if (btnSend) {
          btnSend.disabled = !queryInput.value.trim() || isProcessing;
        }
      });

      // 3. Tangani Shortcut Keyboard: Enter kirim, Shift+Enter baris baru
      queryInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          if (btnSend && !btnSend.disabled && !isProcessing) {
            queryForm.requestSubmit();
          }
        }
      });
    }

    // 4. Tangani Pengiriman Form Pertanyaan
    if (queryForm) {
      queryForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query || isProcessing) return;

        await executeQuery(query);
      });
    }

    // 5. Eksekusi Pertanyaan (Terpusat)
    async function executeQuery(query) {
      lastQuery = query;
      isProcessing = true;
      if (btnSend) btnSend.disabled = true;

      // Sembunyikan empty state pada pertanyaan pertama
      if (emptyState && emptyState.style.display !== "none") {
        emptyState.style.display = "none";
      }

      // Tampilkan pesan pengguna
      if (ui.appendUserMessage) {
        ui.appendUserMessage(conversationContainer, query);
      }

      // Reset input
      if (queryInput) {
        queryInput.value = "";
        queryInput.style.height = "48px";
      }

      // Tampilkan indikator proses
      if (ui.showLoadingIndicator) {
        ui.showLoadingIndicator(conversationContainer);
      }

      try {
        if (!askQuestion) {
          throw new Error("Layanan askQuestion tidak ditemukan.");
        }
        const responseData = await askQuestion(query);
        if (ui.appendAssistantResponse) {
          ui.appendAssistantResponse(conversationContainer, responseData);
        }
      } catch (error) {
        console.error("GITA Query Error:", error);
        if (ui.appendErrorMessage) {
          ui.appendErrorMessage(
            conversationContainer,
            error.message || "Terjadi kendala saat memproses jawaban.",
            () => executeQuery(lastQuery)
          );
        }
      } finally {
        isProcessing = false;
        if (btnSend && queryInput) {
          btnSend.disabled = !queryInput.value.trim();
        }
        if (queryInput) {
          queryInput.focus();
        }
      }
    }

    // 6. Tangani Klik Kartu Contoh Pertanyaan
    samplePromptCards.forEach((card) => {
      card.addEventListener("click", () => {
        const promptText = card.getAttribute("data-prompt") || card.querySelector(".sample-prompt-text")?.textContent;
        if (promptText && !isProcessing) {
          if (queryInput) queryInput.value = promptText;
          executeQuery(promptText);
        }
      });
    });

    // 7. Tombol Reset / Percakapan Baru
    if (btnNewChat) {
      btnNewChat.addEventListener("click", () => {
        if (conversationContainer && conversationContainer.children.length > 0 && !isProcessing) {
          conversationContainer.innerHTML = "";
          if (emptyState) {
            emptyState.style.display = "flex";
          }
          if (queryInput) {
            queryInput.value = "";
            queryInput.style.height = "48px";
            queryInput.focus();
          }
          if (btnSend) btnSend.disabled = true;
          if (ui.scrollToBottom) ui.scrollToBottom();
        }
      });
    }

    // Fokus awal ke textarea input
    if (queryInput) {
      queryInput.focus();
    }
  });
})(typeof window !== 'undefined' ? window : this);
