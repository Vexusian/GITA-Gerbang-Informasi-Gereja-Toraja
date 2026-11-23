/**
 * GITA - Frontend Configuration
 * Universal Vanilla JS Module (Mendukung file:// dan http://)
 */

(function(window) {
  'use strict';

  window.GITA = window.GITA || {};

  window.GITA.CONFIG = {
    // Otomatis aktifkan Live Backend jika dibuka via http/localhost, atau Simulasi jika dibuka offline (file://)
    USE_MOCK: !(typeof window !== 'undefined' && window.location.protocol.startsWith('http')),

    // Endpoint FastAPI Backend
    API_BASE_URL: "http://127.0.0.1:8000/api",
    ENDPOINTS: {
      QUERY: "/query",
      HEALTH: "/health"
    },

    // Batas waktu permintaan (ms)
    TIMEOUT_MS: 20000,

    // Metadata Dokumen
    DOCUMENT_INFO: {
      NAME: "Tata Gereja Toraja",
      CODE: "TGT",
      YEAR: "2018",
      TOTAL_CHUNKS: 146
    }
  };
})(typeof window !== 'undefined' ? window : this);
