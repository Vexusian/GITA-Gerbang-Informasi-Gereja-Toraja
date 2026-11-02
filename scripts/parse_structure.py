import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "processed" / "extracted_pages.json"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "structured_document.json"

# Judul bagian yang menjadi batas struktur dokumen
SECTION_PATTERNS = {
    "Pembukaan": r"^PEMBUKAAN$",
    "Memori Penjelasan": r"^MEMORI PENJELASAN$",
    "Lampiran 2": r"^LAMPIRAN\s+2\b.*$"
}

CHAPTER_PATTERN = r"^BAB\s+([IVXLCDM]+)\s*$"
ARTICLE_PATTERN = r"^Pasal\s+(\d+)\s*:?\s*$"


def parse_document():
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        pages = json.load(file)

    units = []

    current_section = None
    current_chapter = None
    current_unit = None

    def finish_unit():
        """Simpan unit yang sedang dikumpulkan."""
        nonlocal current_unit

        if current_unit:
            current_unit["content"] = "\n".join(
                current_unit["content_lines"]
            ).strip()

            del current_unit["content_lines"]

            if current_unit["content"]:
                units.append(current_unit)

        current_unit = None

    def add_line(text, page_number):
        """Tambahkan teks dan catat halaman sumbernya."""
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

            if re.fullmatch(r"\d{1,3}", text):
                continue

            if not text:
                if current_unit is not None:
                    add_line("", page_number)
                continue

            # 1. Identifikasi judul bagian dokumen.
            # Hanya periksa 12 baris pertama agar tidak salah
            # membaca penyebutan bagian di dalam isi atau daftar isi.
            if line_index < 12:
                section_found = None

                for section, pattern in SECTION_PATTERNS.items():
                    if re.match(pattern, text, re.IGNORECASE):
                        section_found = section
                        break

                if section_found:
                    finish_unit()

                    current_section = section_found
                    current_chapter = None

                    if current_section == "Pembukaan":
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

            # 2. Identifikasi awal Batang Tubuh.
            chapter_match = re.match(
                CHAPTER_PATTERN,
                text,
                re.IGNORECASE
            )

            if chapter_match:
                chapter_number = chapter_match.group(1).upper()

                finish_unit()

                if chapter_number == "I":
                    current_section = "Batang Tubuh"

                if current_section == "Batang Tubuh":
                    current_chapter = chapter_number

                continue

            # 3. Identifikasi Pasal.
            article_match = re.match(
                ARTICLE_PATTERN,
                text,
                re.IGNORECASE
            )

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

            # 4. Kumpulkan isi unit yang sedang diproses.
            add_line(text, page_number)

    # Simpan unit terakhir.
    finish_unit()

    document = {
        "document_title": "Tata Gereja Toraja",
        "source_file": "TGT.pdf",
        "units": units
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            document,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("Parsing selesai!")
    print(f"Total unit: {len(units)}")
    print(f"Output: {OUTPUT_PATH}")

    # Ringkasan jumlah unit berdasarkan bagian.
    summary = {}

    for unit in units:
        section = unit["section"]
        summary[section] = summary.get(section, 0) + 1

    print("\nRingkasan:")
    for section, total in summary.items():
        print(f"- {section}: {total} unit")


if __name__ == "__main__":
    parse_document()