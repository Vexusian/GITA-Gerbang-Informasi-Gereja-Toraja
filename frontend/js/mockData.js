/**
 * GITA - Mock Data Provider
 * Memuat data simulasi autentik berdasarkan dokumen chunks.json Tata Gereja Toraja
 * Menunjang pengujian tampilan untuk 4 status: success, not_found, insufficient_evidence, error
 */

(function(window) {
  'use strict';

  window.GITA = window.GITA || {};

  const MOCK_DATABASE = [
    {
      keywords: ["hakikat", "wujud", "pasal 2", "nama", "pasal 1", "siapa gereja toraja"],
      response: {
        status: "success",
        answer: "Berdasarkan **Tata Gereja Toraja Batang Tubuh BAB I (Pasal 1 & 2)**, berikut adalah hakikat, wujud, dan nama resmi gereja:\n\n1. **Nama Resmi:** Nama gereja ini adalah **Gereja Toraja** (Pasal 1).\n2. **Hakikat:** Gereja Toraja adalah persekutuan orang-orang yang percaya kepada Tuhan Yesus Kristus.\n3. **Penyataan Iman:** Gereja Toraja adalah penyataan dari gereja yang esa, kudus, am, dan rasuli.\n4. **Wujud:** Gereja Toraja mewujud dalam gereja setempat yang disebut **jemaat**.",
        sources: [
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-1",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "1",
            page_start: 10,
            page_end: 10,
            content: "Pasal 1\nNama\nNama gereja ini adalah Gereja Toraja."
          },
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-2",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "2",
            page_start: 10,
            page_end: 10,
            content: "Pasal 2\nHakikat dan Wujud\n1. Gereja Toraja adalah persekutuan orang-orang yang percaya kepada Tuhan Yesus Kristus.\n2. Gereja Toraja adalah penyataan dari gereja yang esa, kudus, am dan rasuli.\n3. Gereja Toraja mewujud dalam gereja setempat yang disebut jemaat."
          }
        ]
      }
    },
    {
      keywords: ["visi", "misi", "tujuan", "bentuk", "presbiterial", "sinodal", "pasal 5", "pasal 6", "pasal 8"],
      response: {
        status: "success",
        answer: "Menurut **Tata Gereja Toraja Batang Tubuh BAB I**:\n\n* **Visi (Pasal 5):** Terwujudnya Gereja Toraja yang memuliakan Tuhan, memberitakan kebaikan-Nya, dan menjadi berkat bagi manusia dan dunia.\n* **Misi (Pasal 6):** Bersekutu, bersaksi, dan melayani.\n* **Tujuan (Pasal 7):** Menghadirkan keadilan dan damai sejahtera dalam ketaatan dan kesetiaan kepada Tuhan.\n* **Bentuk Organisasi (Pasal 8):** Berbentuk **Presbiterial Sinodal**, dengan penataan pelayanan dalam lingkup: jemaat, klasis, sinode wilayah, dan sinode am.",
        sources: [
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-5",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "5",
            page_start: 11,
            page_end: 11,
            content: "Pasal 5\nVisi Gereja Toraja\nVisi Gereja Toraja adalah terwujudnya Gereja Toraja yang memuliakan Tuhan, memberitakan kebaikan-Nya, menjadi berkat bagi manusia dan dunia."
          },
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-6",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "6",
            page_start: 11,
            page_end: 11,
            content: "Pasal 6\nMisi Gereja Toraja\nMisi Gereja Toraja adalah bersekutu, bersaksi, dan melayani."
          },
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-8",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "8",
            page_start: 11,
            page_end: 11,
            content: "Pasal 8\nBentuk\n1. Bentuk Gereja Toraja adalah Presbiterial Sinodal.\n2. Berdasarkan bentuknya, Gereja Toraja menata pelayanannya dalam lingkup jemaat, klasis, sinode wilayah dan sinode am."
          }
        ]
      }
    },
    {
      keywords: ["sejarah", "kapan terbentuk", "status hukum", "kedudukan", "pasal 3", "1947", "akta", "tanah"],
      response: {
        status: "success",
        answer: "Berdasarkan **Tata Gereja Toraja Batang Tubuh Pasal 3** mengenai waktu pembentukan, kedudukan, dan status hukum:\n\n1. **Waktu Pembentukan:** Terbentuk pada tanggal **25 Maret 1947** dalam Sidang Majelis Am yang pertama di Rantepao untuk jangka waktu yang tidak ditentukan.\n2. **Kedudukan:** Berkedudukan di Indonesia dan dapat melayani di tempat-tempat lain.\n3. **Status Badan Hukum:**\n   - Dinyatakan sebagai Lembaga Keagamaan Yang Bersifat Gereja berdasarkan **Keputusan Menteri Agama R.I. No. 26 tanggal 11 Mei 1971**.\n   - Ditetapkan sebagai Badan Hukum yang berhak atas tanah berdasarkan **Keputusan Menteri Dalam Negeri No. 61/DJA/1973**.",
        sources: [
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-3",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "3",
            page_start: 10,
            page_end: 11,
            content: "Pasal 3\nWaktu, Tempat Kedudukan dan Status Hukum\n1. Gereja Toraja sebagai lembaga gerejawi terbentuk pada tanggal 25 Maret 1947 dalam Sidang Majelis Am yang pertama di Rantepao untuk waktu yang tidak ditentukan.\n2. Gereja Toraja berkedudukan di Indonesia dan dapat melayani di tempat-tempat lain.\n3. Gereja Toraja dinyatakan sebagai Lembaga Keagamaan Yang Bersifat Gereja berdasarkan Keputusan Menteri Agama R.I. No.26 tanggal 11 Mei 1971 dan Penunjukan Gereja Toraja sebagai Badan Hukum yang dapat mempunyai Hak Atas Tanah berdasarkan Keputusan Menteri Dalam Negeri no 61/DJA/1973."
          }
        ]
      }
    },
    {
      keywords: ["pengakuan iman", "dasar iman", "pasal 4", "athanasius", "rasuli"],
      response: {
        status: "success",
        answer: "Berdasarkan **Pasal 4 Tata Gereja Toraja**, dasar pengakuan iman Gereja Toraja dirumuskan sebagai berikut:\n\n1. Gereja Toraja mengaku bahwa Yesus Kristus itulah Tuhan dan Juruselamat dunia, Kepala Gereja, sesuai kesaksian Alkitab sebagaimana dirumuskan dalam Pengakuan Iman Gereja Toraja.\n2. Pengakuan Iman Gereja Toraja meliputi:\n   - Pengakuan Gereja Toraja\n   - Pengakuan Iman Rasuli\n   - Pengakuan Athanasius\n   - Pengakuan Nicea Konstantinopel.",
        sources: [
          {
            chunk_id: "TGT-BT-BAB-I-PASAL-4",
            document: "Tata Gereja Toraja",
            section: "Batang Tubuh",
            chapter: "I",
            article: "4",
            page_start: 11,
            page_end: 11,
            content: "Pasal 4\nPengakuan Iman\n1. Gereja Toraja mengaku bahwa Yesus Kristus itulah Tuhan dan Juruselamat dunia, Kepala Gereja, sesuai kesaksian Alkitab sebagaimana dirumuskan dalam Pengakuan Iman Gereja Toraja.\n2. Pengakuan Iman Gereja Toraja meliputi: Pengakuan Gereja Toraja, Pengakuan Iman Rasuli, Pengakuan Athanasius, dan Pengakuan Nicea Konstantinopel."
          }
        ]
      }
    }
  ];

  function getMockResponse(query) {
    const lowerQuery = query.toLowerCase().trim();

    // Trigger simulasi error
    if (lowerQuery.includes("error") || lowerQuery.includes("simulasi error")) {
      return {
        status: "error",
        answer: "Terjadi kendala teknis saat memproses penelusuran dokumen. Silakan periksa koneksi backend atau coba beberapa saat lagi.",
        sources: []
      };
    }

    // Trigger simulasi insufficient evidence
    if (lowerQuery.includes("anggaran") || lowerQuery.includes("biaya") || lowerQuery.includes("gaji") || lowerQuery.includes("rincian uang")) {
      return {
        status: "insufficient_evidence",
        answer: "Pertanyaan mengenai rincian angka biaya atau anggaran belanja operasional tidak memiliki dasar bukti spesifik dalam naskah Tata Gereja Toraja. Dokumen ini hanya mengatur tata kelola perbendaharaan dan pertanggungjawaban umum harta milik gereja.",
        sources: []
      };
    }

    // Cari entri yang cocok berdasarkan kata kunci
    for (const item of MOCK_DATABASE) {
      const isMatch = item.keywords.some(keyword => lowerQuery.includes(keyword));
      if (isMatch) {
        return item.response;
      }
    }

    // Trigger not found state
    return {
      status: "not_found",
      answer: "Tidak ditemukan pasal atau ketentuan yang relevan dalam dokumen resmi Tata Gereja Toraja mengenai topik yang ditanyakan. Dokumen Tata Gereja Toraja berfokus pada ketetapan keorganisasian, jabatan gerejawi, ajaran, dan tata ibadah.",
      sources: []
    };
  }

  window.GITA.MOCK_DATABASE = MOCK_DATABASE;
  window.GITA.getMockResponse = getMockResponse;
})(typeof window !== 'undefined' ? window : this);
