
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "processed" / "extracted_pages.json"

with open(INPUT_PATH, "r", encoding="utf-8") as file:
    pages = json.load(file)

patterns = {
    "Pembukaan": r"^\s*PEMBUKAAN\s*$",
    "Batang Tubuh": r"^\s*BAB I\s*$",
    "Memori Penjelasan": r"^\s*MEMORI PENJELASAN\s*$",
    "Lampiran 2": r"^\s*LAMPIRAN 2\b"
}

for page in pages:
    lines = page["content"].splitlines()

    # Periksa beberapa baris awal halaman
    first_lines = "\n".join(lines[:10]).upper()

    for section, pattern in patterns.items():
        if re.search(pattern, first_lines, re.MULTILINE):
            print(f"Halaman PDF {page['page']}: {section}")