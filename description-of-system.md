# GITA: Gerbang Informasi Gereja Toraja

## Rancangan Sistem

---

## 1. Latar Belakang

Gereja Toraja merupakan organisasi gerejawi yang memiliki struktur organisasi berjenjang, mulai dari Sinode Am, Sinode Wilayah, Klasis, hingga Jemaat. Dalam pelaksanaan kehidupan organisasi, terdapat berbagai unsur dan organisasi yang menjalankan fungsi masing-masing, seperti Majelis Gereja, Badan Pekerja Klasis, Badan Pekerja Sinode Wilayah, Badan Pekerja Sinode, badan verifikasi, serta Organisasi Intra-Gerejawi (OIG) yang meliputi Sekolah Minggu Gereja Toraja (SMGT), Persekutuan Pemuda Gereja Toraja (PPGT), Persekutuan Wanita Gereja Toraja (PWGT), dan Persekutuan Kaum Bapak Gereja Toraja (PKBGT).

Pelaksanaan organisasi tersebut didukung oleh berbagai dokumen yang menjadi dasar tata kelola dan operasional, seperti Tata Gereja Toraja, Peraturan Kepegawaian, peraturan dan pedoman organisasi, AD/ART OIG, tata kerja, SOP, pedoman perlawatan, serta berbagai dokumen kebijakan lainnya.

Namun, Gereja Toraja memiliki cakupan pelayanan yang luas dan tersebar di berbagai wilayah Indonesia. Kondisi sumber daya manusia, pendidikan, sosial-ekonomi, serta ketersediaan dan kemampuan pemanfaatan teknologi pada setiap wilayah tidak selalu sama. Perbedaan tersebut berpotensi menimbulkan kesenjangan pemahaman mengenai tata kelola organisasi dan prosedur operasional, terutama pada tingkat yang memiliki akses lebih terbatas terhadap sumber daya informasi dan teknologi.

Salah satu permasalahan yang dapat ditemukan adalah kesulitan pengurus atau majelis dalam memperoleh dan memahami ketentuan organisasi ketika menghadapi suatu persoalan. Pengurus dapat mengetahui bahwa suatu tindakan memiliki aturan tertentu, tetapi belum tentu mengetahui dokumen, pasal, pihak yang berwenang, atau prosedur yang menjadi dasar tindakan tersebut. Kondisi ini dapat menyebabkan ketergantungan kepada individu tertentu yang dianggap lebih memahami tata kelola organisasi.

Selain persoalan pemahaman aturan, terdapat pula permasalahan dalam penyusunan dokumen administrasi organisasi. Pada akhir tahun, OIG, Majelis, maupun badan pekerja perlu melaksanakan rapat kerja dan mempersiapkan berbagai dokumen, seperti Laporan Pertanggungjawaban (LPJ), konsideran, dan rancangan program kerja. Penyusunan dokumen tersebut membutuhkan kemampuan dalam mengorganisasi informasi, menggunakan aplikasi pengolah dokumen, mengatur format, membuat tabel, serta memastikan dokumen tersusun secara rapi dan konsisten.

Dalam kondisi tertentu, keterbatasan perangkat dan sumber daya manusia yang memiliki kemampuan pengolahan dokumen menyebabkan pekerjaan administratif bergantung pada beberapa individu tertentu. Hal tersebut menjadi semakin sulit ketika individu tersebut tidak selalu berada di lokasi organisasi.

Berdasarkan permasalahan tersebut, dirancang **GITA (Gerbang Informasi Gereja Toraja)**, yaitu sistem berbasis Artificial Intelligence (AI) yang membantu pengurus, majelis, dan unsur organisasi Gereja Toraja dalam memahami tata kelola organisasi serta mempersiapkan dokumen administrasi secara terstruktur.

Sistem dirancang dengan pendekatan **Retrieval-Augmented Generation (RAG)** agar jawaban terkait tata kelola dapat didasarkan pada dokumen resmi yang tersedia. Selain itu, GITA memiliki **Document Assistant** yang membantu pengguna menyusun dokumen organisasi secara modular berdasarkan template yang telah ditentukan dan menghasilkan dokumen akhir dalam format PDF.

AI tidak ditempatkan sebagai pengambil keputusan organisasi. AI berfungsi sebagai alat bantu dalam pencarian informasi, penyusunan, perapian, dan pengolahan bahasa, sedangkan keputusan akhir, validasi fakta, serta persetujuan dokumen tetap berada pada manusia.

---

# 2. Tujuan Sistem

GITA bertujuan untuk:

1. Membantu pengurus, majelis, dan unsur organisasi Gereja Toraja memahami tata kelola dan ketentuan organisasi berdasarkan dokumen resmi.
2. Mengurangi kesenjangan akses terhadap informasi dan pemahaman mengenai aturan organisasi.
3. Membantu pengguna menemukan dasar aturan yang relevan terhadap suatu pertanyaan atau permasalahan.
4. Membantu penyusunan dokumen organisasi seperti LPJ, konsideran, dan rancangan program kerja.
5. Memungkinkan penyusunan dokumen dilakukan secara modular sehingga pekerjaan dapat dilakukan secara bertahap.
6. Mengurangi ketergantungan terhadap individu tertentu dalam pekerjaan administratif.
7. Menghasilkan dokumen dengan struktur dan format yang konsisten.
8. Memastikan keputusan dan isi final tetap berada dalam kendali manusia.

---

# 3. Konsep Utama Sistem

GITA memiliki dua kemampuan utama:

## 3.1. Governance Assistant

Governance Assistant membantu pengguna mencari dan memahami informasi berdasarkan dokumen tata kelola Gereja Toraja.

Contoh pertanyaan:

> "Siapa yang memiliki kewenangan untuk melakukan X?"

> "Apa prosedur yang harus dilakukan untuk Y?"

> "Apa dasar aturan mengenai Z?"

Sistem akan mencari bagian dokumen yang relevan kemudian menghasilkan jawaban berdasarkan sumber tersebut.

---

## 3.2. Document Assistant

Document Assistant membantu pengguna menyusun dokumen organisasi melalui tahapan yang terstruktur.

Contoh dokumen:

- Laporan Pertanggungjawaban (LPJ)
- Rancangan Program Kerja
- Konsideran
- Dokumen administrasi organisasi lain yang memiliki template terstruktur

Pengguna tidak harus menyelesaikan seluruh dokumen dalam satu waktu. Setiap bagian dapat dikerjakan, disimpan, diperiksa, dan dilanjutkan kembali pada waktu berikutnya.

---

# 4. Fitur Sistem

## 4.1. Governance Question Answering

Pengguna dapat mengajukan pertanyaan dalam bahasa natural.

Contoh:

> "Apa tugas Majelis Gereja dalam pelaksanaan X?"

Alur:

```text
Pertanyaan pengguna
        ↓
Pemrosesan pertanyaan
        ↓
Retrieval dokumen relevan
        ↓
LLM
        ↓
Jawaban + sumber