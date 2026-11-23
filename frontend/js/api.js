/**
 * GITA - API Service Client
 * Menangani komunikasi dengan FastAPI Backend atau Mock Provider
 * Universal Vanilla JS Module
 */

(function(window) {
  'use strict';

  window.GITA = window.GITA || {};

  async function askQuestion(query) {
    if (!query || typeof query !== "string" || !query.trim()) {
      throw new Error("Pertanyaan tidak boleh kosong.");
    }

    const config = window.GITA.CONFIG || {};

    // JIKA MODE MOCK DIAKTIFKAN
    if (config.USE_MOCK) {
      // Memberikan jeda waktu retrieval FAISS & LLM (600ms) untuk sensasi UI alami
      await new Promise((resolve) => setTimeout(resolve, 600));
      const getMock = window.GITA.getMockResponse;
      const mockRes = getMock ? getMock(query) : { status: "not_found", answer: "Mock provider belum siap.", sources: [] };
      return validateResponseSchema(mockRes);
    }

    // JIKA TERHUBUNG KE BACKEND FASTAPI
    const controller = new AbortController();
    const timeoutMs = config.TIMEOUT_MS || 20000;
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const url = `${config.API_BASE_URL}${config.ENDPOINTS.QUERY}`;
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ question: query.trim() }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server mengembalikan status ${response.status}: ${errorText || response.statusText}`);
      }

      const data = await response.json();
      return validateResponseSchema(data);
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === "AbortError") {
        throw new Error("Waktu permintaan habis (timeout). Backend tidak merespon dalam batas waktu.");
      }

      throw error;
    }
  }

  function validateResponseSchema(data) {
    if (!data || typeof data !== "object") {
      throw new Error("Format respon server tidak valid.");
    }

    const validStatuses = ["success", "not_found", "insufficient_evidence", "error"];
    const status = validStatuses.includes(data.status) ? data.status : "error";
    const answer = typeof data.answer === "string" ? data.answer : "Tidak ada jawaban yang dihasilkan.";
    const sources = Array.isArray(data.sources) ? data.sources : [];

    return {
      status,
      answer,
      sources
    };
  }

  window.GITA.askQuestion = askQuestion;
})(typeof window !== 'undefined' ? window : this);
