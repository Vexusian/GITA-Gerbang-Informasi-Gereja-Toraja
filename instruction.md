# Prompt: Technology Stack Selection & Course Compliance untuk GITA

Saya sedang mengembangkan proyek **GITA (Gerbang Informasi Gereja Toraja)** untuk mata kuliah yang berfokus pada **AI Engineering**.

Saya ingin Anda bertindak sebagai **AI Solution Architect sekaligus reviewer proyek AI Engineering**.

Tugas Anda bukan hanya memilih teknologi, tetapi menentukan **technology stack yang paling realistis untuk proyek ini**, berdasarkan kebutuhan sistem, materi kuliah Minggu 1–9, keterbatasan hardware, keamanan data, dan batasan scope mata kuliah.

---

# 1. Konteks Proyek

## GITA: Gerbang Informasi Gereja Toraja

GITA adalah **AI-assisted system** yang dirancang untuk membantu akses informasi organisasi, pemahaman tata kelola, dan penyusunan dokumen dalam Gereja Toraja.

Sistem memiliki dua fungsi utama.

### A. Governance Assistant

GITA dapat membantu pengguna memahami informasi organisasi Gereja Toraja berdasarkan dokumen resmi yang tersedia.

Contoh pertanyaan:

* "Apa kewenangan Majelis Gereja dalam hal ini?"
* "Siapa yang berwenang mengambil keputusan tersebut?"
* "Prosedur apa yang harus dilakukan untuk kegiatan tersebut?"
* "Pasal atau dokumen mana yang mengatur hal ini?"
* "Apa perbedaan kewenangan antara Jemaat dan Klasis?"
* "Dokumen apa yang menjadi dasar aturan tersebut?"

Jawaban harus:

* berdasarkan dokumen sumber;
* menyertakan sumber/evidence;
* tidak mengarang aturan;
* tidak membuat kesimpulan jika evidence tidak cukup;
* menyatakan bahwa informasi tidak dapat ditentukan jika sumber yang tersedia tidak mendukung jawaban.

---

### B. Document Assistant

GITA juga membantu pengguna menyiapkan dokumen organisasi seperti:

* notulensi rapat;
* LPJ;
* rancangan program kerja;
* konsideran;
* dan dokumen organisasi lain yang relevan.

Pengguna dapat mengerjakan dokumen secara bertahap.

AI membantu:

* menyusun redaksi;
* merapikan informasi;
* mengubah informasi menjadi struktur dokumen;
* membantu menghasilkan bagian tertentu;
* tetapi **tidak boleh mengarang fakta, angka, keputusan, kegiatan, atau informasi organisasi**.

Hal-hal seperti:

* perhitungan;
* struktur tabel;
* penomoran;
* template;
* layout;
* dan pembuatan PDF

sebisa mungkin dilakukan secara **deterministic oleh program**, bukan diserahkan sepenuhnya kepada LLM.

---

# 2. Multimodal Requirement

Dosen mensyaratkan adanya **multimodal component**.

Use case multimodal yang dipilih adalah:

## Foto Catatan Rapat → Notulensi PDF

Pengguna dapat mengunggah foto:

* catatan rapat;
* catatan tangan;
* papan tulis;
* lembar hasil pembahasan;
* atau catatan kasar lainnya.

GITA kemudian membantu:

**Image**
→ OCR / Vision
→ ekstraksi informasi
→ structured output
→ human verification
→ AI-assisted document generation
→ notulensi
→ PDF

Informasi yang dapat diekstraksi antara lain:

* tanggal;
* agenda;
* peserta jika tersedia;
* topik pembahasan;
* hasil pembahasan;
* keputusan;
* kegiatan;
* penanggung jawab;
* jadwal;
* informasi lain yang benar-benar terdapat pada sumber.

Jika tulisan atau informasi tidak dapat dibaca dengan cukup yakin, sistem harus menandainya untuk **human verification**, bukan menebak.

---

# 3. Prinsip AI Engineering

Gunakan prinsip berikut:

### AI bertanggung jawab atas:

* pemahaman bahasa;
* ekstraksi informasi;
* semantic understanding;
* retrieval-assisted generation;
* penyusunan dan transformasi teks;
* multimodal understanding jika diperlukan.

### Program bertanggung jawab atas:

* validasi;
* perhitungan;
* struktur data;
* template;
* tabel;
* penomoran;
* layout;
* pembuatan PDF;
* access control;
* penyimpanan data;
* workflow.

### Human bertanggung jawab atas:

* validasi fakta;
* validasi hasil OCR/vision;
* validasi hasil AI;
* keputusan organisasi;
* persetujuan dokumen final.

---

# 4. Materi Kuliah Minggu 1–9

Proyek ini harus dapat menunjukkan penerapan materi yang sudah diajarkan sampai **Minggu 9**.

Gunakan **materi kuliah yang saya berikan sebagai sumber utama**, bukan asumsi umum mengenai AI Engineering.

Lakukan mapping eksplisit antara fitur GITA dengan materi Minggu 1–9.

Minimal periksa kemungkinan penerapan:

* penggunaan dan pemilihan model AI;
* LLM;
* token/context;
* prompt design;
* prompt engineering;
* structured output;
* schema/validation;
* hallucination;
* grounding;
* RAG;
* embeddings;
* chunking;
* retrieval;
* similarity;
* metadata;
* tools/function calling jika memang relevan;
* agentic behavior jika memang relevan;
* multimodal AI;
* human-in-the-loop;
* testing/evaluation;
* guardrails;
* dan konsep lain yang benar-benar terdapat dalam materi Minggu 1–9.

**Jangan memasukkan teknologi atau konsep hanya untuk membuat proyek terlihat lebih canggih.**

Jika suatu materi tidak perlu atau tidak cocok diterapkan pada GITA, jelaskan alasannya.

Jika suatu konsep belum diajarkan sampai Minggu 9, jangan menjadikannya komponen wajib.

---

# 5. Persyaratan UTS

Proyek harus dapat digunakan untuk menjawab dan mempertahankan pertanyaan/instruksi yang mungkin muncul pada UTS.

Pastikan rancangan sistem dapat menjelaskan dengan jelas:

1. **Problem**

   * masalah nyata apa yang diselesaikan GITA;
   * siapa pengguna;
   * mengapa masalah tersebut membutuhkan AI.

2. **Why Generative AI**

   * mengapa menggunakan generative AI;
   * mengapa pendekatan non-generative tidak cukup;
   * bagian mana yang cocok menggunakan LLM;
   * bagian mana yang seharusnya tidak menggunakan LLM.

3. **System Design**

   * komponen sistem;
   * alur data;
   * hubungan antar komponen;
   * input → processing → output.

4. **Output Control**

   * bagaimana mengontrol output AI;
   * structured output;
   * validation;
   * schema;
   * fallback;
   * guardrails.

5. **Tools**

   * apakah GITA membutuhkan tools/function calling;
   * tool apa yang digunakan;
   * mengapa tool tersebut diperlukan;
   * apakah tool bersifat read-only atau write;
   * apakah human approval diperlukan sebelum write action.

6. **Grounding**

   * bagaimana sistem mencegah hallucination;
   * bagaimana sumber informasi diberikan;
   * bagaimana sistem menangani evidence yang tidak cukup.

7. **Evidence & Testing**

   * bagaimana kualitas sistem diuji;
   * bagaimana retrieval dievaluasi;
   * bagaimana jawaban AI diverifikasi;
   * bagaimana multimodal extraction diuji;
   * contoh failure cases.

8. **Risks & Limitations**

   * hallucination;
   * OCR/vision errors;
   * incorrect retrieval;
   * dokumen versi lama;
   * data sensitif;
   * incorrect structured output;
   * keterbatasan local LLM;
   * keterbatasan hardware.

Saya ingin desain ini dapat dipertahankan secara logis ketika dosen bertanya **"mengapa memilih teknologi tersebut?"**, bukan sekadar "karena populer".

---

# 6. Hardware Constraint

GITA akan dikembangkan dan dijalankan **secara lokal pada laptop saya**.

Spesifikasi:

* **GPU:** NVIDIA RTX 2050
* **CPU:** Intel Core i5 Gen 12
* **RAM:** 12 GB
* **Storage:** 474 GB
* **OS:** Windows

Anggap GPU memiliki VRAM terbatas dan RAM sistem juga terbatas.

Jangan merekomendasikan model atau stack yang secara realistis tidak dapat dijalankan pada hardware tersebut.

Jika GPU/VRAM menjadi bottleneck, jelaskan:

* apakah model dapat berjalan CPU;
* apakah membutuhkan quantization;
* ukuran model yang realistis;
* kebutuhan RAM/VRAM;
* perkiraan trade-off kualitas vs kecepatan;
* apakah sebagian proses sebaiknya dijalankan CPU;
* apakah OCR/embedding/LLM perlu dipisahkan.

---

# 7. Local-First Requirement

Untuk tahap awal, GITA harus **local-first**.

Prioritas:

1. Data Gereja Toraja tidak dikirim ke cloud eksternal.
2. Dokumen sensitif tetap tersimpan lokal.
3. LLM sebisa mungkin berjalan lokal.
4. Embedding sebisa mungkin lokal.
5. Database lokal.
6. Vector database lokal.
7. OCR/vision sebisa mungkin lokal.
8. Tidak bergantung pada API berbayar untuk menjalankan MVP.

Namun jangan memaksakan local AI jika hasilnya secara signifikan tidak memadai.

Berikan analisis:

> **Apakah local AI cukup mumpuni untuk GITA pada hardware saya?**

Nilai berdasarkan:

* bahasa Indonesia;
* instruction following;
* RAG;
* document understanding;
* structured output;
* hallucination;
* multimodal capability;
* inference speed;
* RAM/VRAM;
* quantization;
* privacy.

Jika ada bagian yang lebih baik menggunakan cloud, jelaskan secara eksplisit, tetapi tetap berikan **local-first recommendation**.

---

# 8. Teknologi yang Harus Dievaluasi

Pilih teknologi berdasarkan kebutuhan, bukan popularitas.

## A. Programming Language

Bandingkan secara relevan:

* Python
* PHP
* JavaScript/TypeScript

atau alternatif lain jika benar-benar diperlukan.

Pertimbangkan:

* AI/ML ecosystem;
* RAG;
* OCR;
* LLM integration;
* document processing;
* backend;
* maintainability;
* learning curve;
* suitability untuk mahasiswa.

---

## B. Backend Framework

Evaluasi misalnya:

* FastAPI
* Django
* Laravel

atau alternatif lain.

Pertimbangkan:

* AI integration;
* API;
* authentication;
* file upload;
* asynchronous processing;
* database;
* maintainability;
* complexity.

---

## C. Frontend

Evaluasi apakah cukup menggunakan:

* server-rendered interface;
* Blade;
* React;
* Vue;
* Svelte;

atau alternatif lain.

Jangan memilih SPA framework hanya karena populer.

Pertimbangkan kebutuhan nyata GITA.

---

## D. Starter Kit

Tentukan apakah starter kit diperlukan.

Jika diperlukan, evaluasi pilihan yang relevan untuk framework yang dipilih.

Pertimbangkan apakah starter kit membantu:

* authentication;
* authorization;
* user management;
* dashboard;

atau justru menambah kompleksitas.

---

## E. LLM

Ini harus dianalisis sangat serius.

Bandingkan beberapa kandidat **local/open-weight model** yang realistis terhadap:

* RTX 2050;
* RAM 12 GB;
* kebutuhan bahasa Indonesia;
* RAG;
* structured output;
* document summarization;
* formal writing;
* hallucination;
* context window;
* quantization;
* inference speed;
* license;
* local deployment.

Jangan otomatis memilih model terbesar.

Berikan:

* kandidat terbaik untuk hardware saya;
* kandidat terbaik untuk kualitas;
* kandidat paling seimbang;
* kandidat yang sebaiknya dihindari dan alasannya.

---

## F. Embedding Model

Pilih embedding model yang cocok untuk:

* Bahasa Indonesia;
* semantic search;
* RAG;
* dokumen organisasi.

Pertimbangkan local execution dan kebutuhan resource.

---

## G. Vector Database

Evaluasi:

* PostgreSQL + pgvector;
* Qdrant;
* Chroma;
* FAISS;

atau alternatif lain.

Pertimbangkan:

* local deployment;
* persistence;
* metadata filtering;
* semantic search;
* scalability;
* simplicity.

---

## H. Relational Database

Evaluasi:

* PostgreSQL;
* MySQL/MariaDB;

untuk data:

* user;
* role;
* dokumen;
* metadata;
* project document;
* section;
* progress;
* template;
* audit log.

Berikan satu pilihan final.

---

## I. Local AI Runtime

Evaluasi:

* Ollama;
* llama.cpp;
* vLLM;
* atau alternatif lain.

Pertimbangkan hardware saya.

Bedakan:

* development;
* MVP;
* future production.

---

## J. RAG Framework

Evaluasi:

* LangChain;
* LlamaIndex;
* Haystack;
* custom/simple implementation.

Jangan menganggap framework selalu diperlukan.

Pilih pendekatan dengan kompleksitas yang sesuai dengan proyek mahasiswa dan materi kuliah.

---

## K. OCR / Vision

Evaluasi teknologi lokal yang realistis untuk membaca:

* foto catatan rapat;
* tulisan tangan jika memungkinkan;
* printed text;
* tabel;
* dokumen.

Pertimbangkan:

* OCR engine;
* vision-language model;
* kualitas Bahasa Indonesia;
* handwritten text;
* hardware;
* latency.

Tentukan apakah lebih tepat menggunakan:

**OCR → LLM**

atau:

**Vision-Language Model → structured output**

atau kombinasi keduanya.

---

## L. Document Processing

Pilih teknologi untuk:

* DOCX;
* PDF;
* template;
* table generation;
* document generation;
* PDF generation.

Tentukan bagian mana yang AI dan bagian mana yang deterministic.

---

## M. Authentication & Authorization

Tentukan pendekatan untuk:

* authentication;
* authorization;
* RBAC;
* akses dokumen;
* audit log.

---

## N. Deployment

Rancang deployment lokal sederhana.

Pertimbangkan:

* Docker;
* Docker Compose;
* local services;
* backend;
* database;
* vector database;
* model runtime.

Jangan menggunakan arsitektur microservices hanya karena terlihat keren.

---

# 9. Security & Privacy

Karena data dapat berupa dokumen internal Gereja Toraja, analisis:

* authentication;
* authorization;
* RBAC;
* file access control;
* local storage;
* audit log;
* model/API privacy;
* data leakage;
* prompt injection pada dokumen;
* malicious document;
* model output risks.

Berikan rekomendasi yang masih realistis untuk MVP.

---

# 10. Tools / Function Calling

Analisis apakah GITA membutuhkan tools/function calling.

Contoh kemungkinan:

* `search_documents()`
* `get_document_metadata()`
* `get_document_section()`
* `save_document_section()`
* `generate_document()`
* `calculate_budget()`
* `export_pdf()`

Namun jangan membuat tools yang sebenarnya tidak diperlukan.

Untuk setiap tool, tentukan:

* tujuan;
* input;
* output;
* read/write;
* apakah memerlukan human approval.

---

# 11. Agentic Behavior

Evaluasi apakah GITA benar-benar membutuhkan agent.

Jangan membuat agent hanya karena agentic AI sedang populer.

Jika workflow biasa sudah cukup, katakan bahwa agent tidak diperlukan.

Jika agent diperlukan, jelaskan:

* goal;
* tools;
* decision loop;
* batasan;
* human approval;
* failure handling.

---

# 12. Evaluation & Testing

Rancang testing yang sesuai dengan GITA.

Minimal pertimbangkan:

### RAG

* retrieval accuracy;
* relevance;
* groundedness;
* citation correctness;
* insufficient evidence handling.

### LLM

* instruction following;
* hallucination;
* structured output validity;
* consistency.

### Multimodal

* OCR accuracy;
* extraction accuracy;
* incorrect/ambiguous handwriting;
* missing information.

### Document Assistant

* apakah AI mengarang fakta;
* apakah informasi pengguna dipertahankan;
* apakah template sesuai;
* apakah PDF valid.

Berikan contoh test cases dan failure cases.

---

# 13. Technology Decision Matrix

Buat tabel perbandingan teknologi.

Minimal:

| Komponen | Kandidat | Kelebihan | Kekurangan | Resource | Cocok untuk GITA? | Keputusan |
| -------- | -------- | --------- | ---------- | -------- | ----------------- | --------- |

Gunakan penilaian yang realistis.

---

# 14. Final Recommended Stack

Setelah seluruh analisis, berikan **SATU stack utama**.

Format:

| Layer               | Technology |
| ------------------- | ---------- |
| Language            |            |
| Backend             |            |
| Frontend            |            |
| Starter Kit         |            |
| LLM                 |            |
| LLM Runtime         |            |
| Embedding           |            |
| RAG                 |            |
| Vector DB           |            |
| Relational DB       |            |
| OCR/Vision          |            |
| Document Processing |            |
| PDF Generation      |            |
| Authentication      |            |
| Deployment          |            |

Kemudian jelaskan alasan setiap keputusan.

---

# 15. Architecture

Buat architecture diagram berbentuk Mermaid.

Minimal menggambarkan:

```text
User
 ↓
Frontend
 ↓
Backend
 ├── Governance Assistant
 │      ↓
 │    Query
 │      ↓
 │    Retrieval
 │      ↓
 │    Vector DB
 │      ↓
 │    Context
 │      ↓
 │    Local LLM
 │      ↓
 │    Grounded Answer + Sources
 │
 ├── Document Assistant
 │      ↓
 │    Structured Input / AI Assistance
 │      ↓
 │    Validation
 │      ↓
 │    Template
 │      ↓
 │    PDF
 │
 └── Multimodal Meeting Notes
        ↓
      Image
        ↓
     OCR/Vision
        ↓
  Structured Extraction
        ↓
   Human Verification
        ↓
   Notulensi Generator
        ↓
        PDF

Database
Vector Database
Local Model Runtime
```

Sesuaikan diagram dengan teknologi final yang dipilih.

---

# 16. MVP Scope

Tentukan dengan ketat mana yang masuk MVP.

Bagi menjadi:

### MUST HAVE

Fitur yang wajib untuk memenuhi tujuan proyek dan materi.

### SHOULD HAVE

Fitur yang meningkatkan kualitas tetapi tidak wajib.

### FUTURE

Fitur yang sebaiknya tidak dimasukkan ke MVP karena terlalu kompleks.

Pastikan MVP masih realistis dijalankan pada:

**RTX 2050 + i5 Gen 12 + RAM 12 GB.**

---

# 17. Course Compliance Matrix

Buat tabel:

| Materi Minggu | Konsep | Implementasi pada GITA | Bukti/Feature | Status |
| ------------- | ------ | ---------------------- | ------------- | ------ |

Gunakan **hanya konsep yang benar-benar terdapat dalam materi kuliah yang saya berikan**.

Tandai:

* Implemented
* Partially Implemented
* Not Needed
* Not Covered Yet

Jangan mengklaim sebuah konsep sudah diterapkan jika sebenarnya hanya disebutkan secara teoritis.

---

# 18. UTS Defense Checklist

Setelah menentukan stack, buat daftar pertanyaan yang kemungkinan dapat ditanyakan dosen berdasarkan rancangan GITA.

Untuk setiap pertanyaan berikan:

**Pertanyaan → Jawaban singkat → Alasan teknis → Bukti di sistem**

Contoh kategori:

* Mengapa menggunakan LLM?
* Mengapa tidak menggunakan model biasa?
* Mengapa local model?
* Apakah local model cukup bagus?
* Mengapa menggunakan RAG?
* Mengapa tidak fine-tuning?
* Bagaimana mencegah hallucination?
* Bagaimana sistem tahu jawaban berasal dari dokumen?
* Bagaimana menangani dokumen yang tidak relevan?
* Mengapa menggunakan embedding?
* Mengapa menggunakan vector database?
* Bagaimana chunking dilakukan?
* Mengapa memilih model tersebut?
* Bagaimana mengontrol output?
* Mengapa menggunakan structured output?
* Mengapa membutuhkan multimodal?
* Mengapa foto catatan rapat?
* Bagaimana menangani OCR yang salah?
* Di mana human-in-the-loop?
* Apakah sistem membutuhkan agent?
* Apa tools/function calling yang digunakan?
* Apa yang terjadi jika AI tidak menemukan evidence?
* Bagaimana menjaga keamanan dokumen?
* Mengapa database tersebut dipilih?
* Mengapa framework tersebut dipilih?
* Mengapa teknologi X tidak dipilih?
* Apa keterbatasan sistem?
* Bagaimana melakukan testing?

Tambahkan pertanyaan lain yang relevan berdasarkan materi Minggu 1–9.

---

# 19. Scope Control

Ini sangat penting.

Saya **tidak ingin proyek ini keluar dari materi kuliah**.

Karena itu:

1. Prioritaskan materi Minggu 1–9.
2. Jangan menambahkan teknologi AI yang belum diperlukan.
3. Jangan menambahkan arsitektur kompleks tanpa alasan.
4. Jangan menggunakan fine-tuning jika RAG/prompting sudah cukup.
5. Jangan menggunakan agent jika workflow deterministik sudah cukup.
6. Jangan menggunakan cloud API jika local deployment cukup.
7. Jangan menambahkan microservices jika monolith/local services cukup.
8. Jangan memilih framework karena popularitas.
9. Jangan memilih model karena benchmark semata.
10. Setiap komponen harus mempunyai alasan berdasarkan kebutuhan GITA.

Jika ada fitur yang menarik tetapi **tidak diperlukan untuk memenuhi problem, materi, atau UTS**, rekomendasikan untuk dikeluarkan dari MVP.

---

# 20. Output Akhir

Berikan jawaban dalam urutan:

1. **Executive Summary**
2. **Understanding of GITA**
3. **Hardware Feasibility**
4. **Local AI Feasibility**
5. **Technology Comparison**
6. **Final Technology Stack**
7. **Architecture**
8. **RAG Design**
9. **Multimodal Design**
10. **Document Assistant Design**
11. **Security & Privacy**
12. **Tools / Function Calling**
13. **Agent Decision**
14. **Evaluation & Testing**
15. **MVP Scope**
16. **Course Compliance Matrix Minggu 1–9**
17. **UTS Defense Checklist**
18. **Risks & Limitations**
19. **Final Recommendation**

### Aturan penting

Jangan memberikan rekomendasi yang terlalu umum.

Untuk setiap keputusan teknologi, jawab:

> **"Mengapa teknologi ini dipilih untuk GITA, pada hardware saya, dan berdasarkan materi yang sudah dipelajari?"**

Jika ada trade-off, jelaskan.

Jika informasi dari materi kuliah tidak cukup untuk menentukan sesuatu, katakan bahwa informasi tersebut tidak tersedia dalam materi dan pisahkan antara:

* **berdasarkan materi kuliah**
* **berdasarkan pertimbangan teknis**
* **berdasarkan rekomendasi arsitektur**

Tujuan akhirnya adalah menghasilkan **stack yang benar-benar dapat saya implementasikan secara lokal di laptop saya, realistis untuk proyek mahasiswa, sesuai materi Minggu 1–9, dapat dipertanggungjawabkan pada UTS, dan tidak overengineered.**
