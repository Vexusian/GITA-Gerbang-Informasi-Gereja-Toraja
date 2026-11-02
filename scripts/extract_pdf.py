import json
from pathlib import Path
import pymupdf

# Direktori utama proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# Lokasi dokumen PDF
PDF_PATH = BASE_DIR / "data" / "documents" / "TGT.pdf"

# Lokasi penyimpanan hasil ekstraksi
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "extracted_pages.json"


def extract_pdf():
    if not PDF_PATH.exists():
        print(f"PDF tidak ditemukan: {PDF_PATH}")
        return

    pages = []

    with pymupdf.open(PDF_PATH) as pdf:
        print(f"Jumlah halaman: {len(pdf)}")

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            pages.append({
                "page": page_number,
                "content": text
            })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            pages,
            file,
            ensure_ascii=False,
            indent=4
        )

    empty_pages = [
        page["page"]
        for page in pages
        if not page["content"]
    ]

    print("\nEkstraksi selesai!")
    print(f"Total halaman: {len(pages)}")
    print(f"Halaman kosong: {empty_pages}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    extract_pdf()
