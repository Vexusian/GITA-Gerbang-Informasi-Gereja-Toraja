"""
Pipeline Otomatis Pemrosesan Dokumen (Automated Document Ingestion Pipeline)
GITA - Gerbang Informasi Tata Gereja Toraja

Fungsi:
1. Menerima input dokumen PDF apa saja secara fleksibel melalui argumen CLI.
2. Mengekstrak teks per halaman menggunakan PyMuPDF.
3. Deteksi Struktur Cerdas (Smart Structure Detection):
   - Jika dokumen memiliki pola BAB & Pasal -> Parsing per Pasal secara utuh.
   - Jika dokumen bebas/tanpa pasal -> Fallback ke chunking berbasis Heading/Paragraf.
4. Memberikan ID unik dinamis berbasis nama file dokumen (misal: TGT-BT-BAB-I-PASAL-1).
5. Mendukung multi-dokumen (Append & Update) pada chunks.json tanpa merusak dokumen lain.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import pymupdf

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DOC = BASE_DIR / "data" / "documents" / "TGT.pdf"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHUNKS_FILE = PROCESSED_DIR / "chunks.json"
REGISTRY_FILE = PROCESSED_DIR / "documents_registry.json"

# Pola Regex Struktur Regulasi Formal
CHAPTER_PATTERN = r"^BAB\s+([IVXLCDM]+)\s*$"
ARTICLE_PATTERN = r"^Pasal\s+(\d+)\s*:?\s*$"

SECTION_PATTERNS = {
    "Pembukaan": r"^PEMBUKAAN$",
    "Batang Tubuh": r"^BATANG\s+TUBUH$",
    "Memori Penjelasan": r"^MEMORI\s+PENJELASAN$",
    "Lampiran": r"^LAMPIRAN\b.*$"
}


def clean_doc_code(filename: str) -> str:
    """Mengubah nama file menjadi kode awalan ID (contoh: 'TGT.pdf' -> 'TGT')."""
    stem = Path(filename).stem
    clean = re.sub(r"[^A-Za-z0-9]", "_", stem).upper()
    return clean[:12]


def extract_pages(pdf_path: Path):
    """Mengekstrak teks mentah per halaman dari file PDF."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"File PDF tidak ditemukan: {pdf_path}")

    pages = []
    with pymupdf.open(pdf_path) as pdf:
        total_pages = len(pdf)
        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()
            pages.append({
                "page": page_num,
                "content": text
            })
    return pages, total_pages


def check_has_articles(pages) -> bool:
    """
    Memeriksa apakah dokumen memiliki struktur formal Pasal.
    Digunakan untuk menentukan strategi chunking (Pasal vs Fallback).
    """
    article_hits = 0
    for page in pages:
        for line in page["content"].splitlines():
            if re.match(ARTICLE_PATTERN, line.strip(), re.IGNORECASE):
                article_hits += 1
                if article_hits >= 3:
                    return True
    return False


def parse_structural_document(pages, doc_title: str, source_filename: str):
    """
    Strategi Utama: Pemotongan berbasis struktur hierarki Bab dan Pasal.
    Menjaga klausul hukum tetap utuh dan menggabungkan pasal lintas halaman.
    """
    units = []
    current_section = "Batang Tubuh"
    current_chapter = None
    current_unit = None

    def finish_unit():
        nonlocal current_unit
        if current_unit:
            current_unit["content"] = "\n".join(current_unit["content_lines"]).strip()
            del current_unit["content_lines"]
            if current_unit["content"]:
                units.append(current_unit)
        current_unit = None

    def add_line(text, page_number):
        if current_unit is None:
            return
        current_unit["content_lines"].append(text)
        if page_number not in current_unit["pages"]:
            current_unit["pages"].append(page_number)
        current_unit["page_end"] = page_number

    for page in pages:
        page_number = page["page"]
        lines = page["content"].splitlines()

        for line_index, line in enumerate(lines):
            text = line.strip()

            # Lewati nomor halaman footer (angka 1-3 digit)
            if re.fullmatch(r"\d{1,3}", text):
                continue

            if not text:
                if current_unit is not None:
                    add_line("", page_number)
                continue

            # 1. Deteksi Judul Bagian Besar (hanya di baris-baris awal halaman)
            if line_index < 12:
                section_found = None
                for sec_name, pattern in SECTION_PATTERNS.items():
                    if re.search(pattern, text, re.IGNORECASE):
                        section_found = sec_name
                        if "Lampiran" in text:
                            section_found = text.split("\n")[0].strip()
                        break

                if section_found:
                    finish_unit()
                    current_section = section_found
                    current_chapter = None

                    if "Pembukaan" in current_section:
                        current_unit = {
                            "type": "section",
                            "section": current_section,
                            "chapter": None,
                            "article": None,
                            "page_start": page_number,
                            "page_end": page_number,
                            "pages": [],
                            "content_lines": []
                        }
                        add_line(text, page_number)
                    continue

            # 2. Deteksi BAB
            chapter_match = re.match(CHAPTER_PATTERN, text, re.IGNORECASE)
            if chapter_match:
                chapter_number = chapter_match.group(1).upper()
                finish_unit()
                if chapter_number == "I" and current_section != "Memori Penjelasan":
                    current_section = "Batang Tubuh"
                current_chapter = chapter_number
                continue

            # 3. Deteksi Pasal
            article_match = re.match(ARTICLE_PATTERN, text, re.IGNORECASE)
            if article_match:
                finish_unit()
                current_unit = {
                    "type": "article",
                    "section": current_section,
                    "chapter": current_chapter,
                    "article": article_match.group(1),
                    "page_start": page_number,
                    "page_end": page_number,
                    "pages": [],
                    "content_lines": []
                }
                add_line(text, page_number)
                continue

            # 4. Tambahkan isi teks ke unit yang sedang aktif
            add_line(text, page_number)

    finish_unit()
    return units


def parse_fallback_document(pages, doc_title: str, source_filename: str):
    """
    Strategi Fallback (Rencana Cadangan):
    Digunakan untuk dokumen bebas yang tidak memiliki Bab & Pasal.
    Memotong berdasarkan paragraf dengan batas ukuran aman (800-1200 karakter).
    """
    chunks = []
    chunk_index = 1

    current_text_blocks = []
    current_char_count = 0
    start_page = None
    end_page = None

    def flush_block():
        nonlocal current_text_blocks, current_char_count, chunk_index, start_page, end_page
        if not current_text_blocks:
            return

        full_content = "\n\n".join(current_text_blocks).strip()
        if full_content:
            chunks.append({
                "type": "paragraph_block",
                "section": "Umum",
                "chapter": None,
                "article": None,
                "page_start": start_page,
                "page_end": end_page,
                "pages": list(range(start_page, end_page + 1)),
                "content": full_content
            })
            chunk_index += 1

        current_text_blocks = []
        current_char_count = 0
        start_page = None
        end_page = None

    for page in pages:
        page_num = page["page"]
        paragraphs = [p.strip() for p in page["content"].split("\n\n") if p.strip()]

        for p in paragraphs:
            if not p:
                continue

            if start_page is None:
                start_page = page_num
            end_page = page_num

            current_text_blocks.append(p)
            current_char_count += len(p)

            # Jika panjang sudah mencapai batas wajar (~1000 karakter), simpan chunk
            if current_char_count >= 1000:
                flush_block()

    flush_block()
    return chunks


def build_chunk_id(unit, doc_prefix: str, index: int) -> str:
    """Menghasilkan chunk_id unik dan terbaca manusia secara dinamis."""
    section = unit.get("section") or "SEC"
    
    # Singkatan kode bagian yang sering muncul
    if "Pembukaan" in section:
        sec_code = "PB"
    elif "Batang Tubuh" in section:
        sec_code = "BT"
    elif "Memori Penjelasan" in section:
        sec_code = "MP"
    elif "Lampiran" in section:
        sec_code = "L2" if "2" in section else "LMP"
    else:
        sec_code = re.sub(r"[^A-Za-z0-9]", "", section).upper()[:3] or "SEC"

    chapter = unit.get("chapter")
    article = unit.get("article")

    if unit.get("type") == "section":
        return f"{doc_prefix}-{sec_code}"

    if article:
        if chapter:
            return f"{doc_prefix}-{sec_code}-BAB-{chapter}-PASAL-{article}"
        return f"{doc_prefix}-{sec_code}-PASAL-{article}"

    return f"{doc_prefix}-{sec_code}-CHUNK-{index:03d}"


def ingest_document(pdf_path_str: str = None):
    """Fungsi utama untuk memproses dokumen secara otomatis."""
    if pdf_path_str:
        pdf_path = Path(pdf_path_str).resolve()
    else:
        pdf_path = DEFAULT_DOC

    if not pdf_path.exists():
        print(f"[ERROR] File PDF tidak ditemukan: {pdf_path}")
        return False

    filename = pdf_path.name
    doc_prefix = clean_doc_code(filename)
    doc_title = Path(filename).stem.replace("_", " ").replace("-", " ").title()

    print(f"\n=======================================================")
    print(f" Memulai Ingestion Pipeline Otomatis: {filename}")
    print(f" Dokumen Prefix: {doc_prefix}")
    print(f" Lokasi: {pdf_path}")
    print(f"=======================================================")

    # 1. Ekstraksi Teks PDF
    print("[1/4] Mengekstrak teks dari halaman PDF...")
    pages, total_pages = extract_pages(pdf_path)
    print(f"      -> Total halaman diekstrak: {total_pages}")

    # 2. Deteksi Struktur
    has_articles = check_has_articles(pages)
    strategy = "structural_article" if has_articles else "fallback_paragraph"
    print(f"[2/4] Menganalisis struktur dokumen...")
    print(f"      -> Format terdeteksi: {'Regulasi Berpasal (BAB/Pasal)' if has_articles else 'Teks Bebas (Fallback)'}")
    print(f"      -> Strategi: {strategy}")

    # 3. Parsing & Chunking
    print("[3/4] Melakukan pemotongan dokumen (chunking)...")
    if has_articles:
        raw_units = parse_structural_document(pages, doc_title, filename)
    else:
        raw_units = parse_fallback_document(pages, doc_title, filename)

    new_chunks = []
    for idx, unit in enumerate(raw_units, start=1):
        content = unit["content"].strip()
        if not content:
            continue

        chunk_id = build_chunk_id(unit, doc_prefix, idx)
        new_chunks.append({
            "chunk_id": chunk_id,
            "document": doc_title,
            "source": filename,
            "type": unit["type"],
            "section": unit["section"],
            "chapter": unit["chapter"],
            "article": unit["article"],
            "page_start": unit["page_start"],
            "page_end": unit["page_end"],
            "content": content
        })

    print(f"      -> Berhasil membuat {len(new_chunks)} chunk.")

    # 4. Multi-Dokumen Aggregation (Append & Update)
    print("[4/4] Memperbarui koleksi chunks.json & registry...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    existing_chunks = []
    if CHUNKS_FILE.exists():
        try:
            with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
                existing_chunks = json.load(f)
        except Exception:
            existing_chunks = []

    # Hapus chunk lama dari file yang sama agar tidak duplikat (update), pertahankan dokumen lain
    filtered_chunks = [c for c in existing_chunks if c.get("source") != filename]
    final_chunks = filtered_chunks + new_chunks

    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, ensure_ascii=False, indent=4)

    # Catat ke Registry Dokumen
    registry = {}
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception:
            registry = {}

    registry[filename] = {
        "title": doc_title,
        "prefix": doc_prefix,
        "total_pages": total_pages,
        "total_chunks": len(new_chunks),
        "strategy": strategy,
        "last_ingested": datetime.now().isoformat()
    }

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=4)

    print("\n-------------------------------------------------------")
    print(f" [SUKSES] Dokumen '{filename}' berhasil di-ingest!")
    print(f" Chunk baru ditambahkan : {len(new_chunks)}")
    print(f" Total chunk di sistem  : {len(final_chunks)}")
    print(f" Tersimpan di          : {CHUNKS_FILE}")
    print(f" Registry dokumen      : {REGISTRY_FILE}")
    print(f"-------------------------------------------------------\n")
    return True


if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else None
    ingest_document(target_file)
