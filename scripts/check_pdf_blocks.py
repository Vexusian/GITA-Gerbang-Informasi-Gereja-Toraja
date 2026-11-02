from pathlib import Path
import sys
import pymupdf

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "data" / "documents" / "TGT.pdf"

if len(sys.argv) < 2:
    print("Gunakan: python scripts/check_pdf_blocks.py <nomor_halaman>")
    sys.exit()

page_number = int(sys.argv[1])

with pymupdf.open(PDF_PATH) as pdf:
    if page_number < 1 or page_number > len(pdf):
        print("Nomor halaman tidak valid.")
        sys.exit()

    page = pdf[page_number - 1]
    blocks = page.get_text("blocks")

    print(f"Halaman PDF: {page_number}")

    for i, block in enumerate(blocks):
        x0, y0, x1, y1, text = block[:5]

        print(f"\nBLOCK {i + 1}")
        print(f"Posisi: x0={x0:.1f}, y0={y0:.1f}, x1={x1:.1f}, y1={y1:.1f}")
        print(text[:500])