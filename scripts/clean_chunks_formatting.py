"""
Skrip Pembersih Format Ayat dan Perapihan Paragraf pada Dokumen TGT
Membersihkan pemisahan baris antara nomor ayat (1., 2., dll) dan isi kalimat ayat,
serta menyambungkan baris kalimat yang terpotong di tengah kalimat dari ekstraksi PDF.
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

CHUNKS_PATH = PROCESSED_DIR / "chunks.json"
FAISS_META_PATH = PROCESSED_DIR / "faiss_metadata.json"
STRUCTURED_PATH = PROCESSED_DIR / "structured_document.json"


def clean_legal_text(content: str) -> str:
    if not content:
        return ""

    raw_lines = [line.strip() for line in content.replace("\r\n", "\n").split("\n")]
    # Hapus baris kosong berlebih
    lines = [l for l in raw_lines if l]

    # Langkah 1: Gabungkan nomor ayat/item yang terisolasi di baris tersendiri
    # Contoh: '1.' di baris 1 dan 'Gereja Toraja...' di baris 2 -> '1. Gereja Toraja...'
    merged_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Pola nomor ayat: 1., (1), a., (a), Ayat 1.
        is_isolated_num = bool(re.match(r"^(\d+\.|\(\d+\)|[a-zA-Z]\.|\([a-zA-Z]\)|Ayat\s+\d+\.?)$", line, re.IGNORECASE))
        if is_isolated_num and i + 1 < len(lines):
            merged_lines.append(f"{line} {lines[i+1]}")
            i += 2
        else:
            merged_lines.append(line)
            i += 1

    # Langkah 2: Satukan baris-baris terpotong dalam satu ayat/paragraf
    blocks = []
    current_block = ""

    for line in merged_lines:
        is_header = bool(re.match(r"^(Pasal\s+\d+|BAB\s+[IVXLCDM]+|PEMBUKAAN|MEMORI\s+PENJELASAN|LAMPIRAN)", line, re.IGNORECASE))
        is_ayat_item = bool(re.match(r"^(\d+\.|\(\d+\)|[a-zA-Z]\.|\([a-zA-Z]\)|Ayat\s+\d+)", line, re.IGNORECASE))

        if is_header:
            if current_block:
                blocks.append(current_block)
                current_block = ""
            blocks.append(line)
            continue

        if is_ayat_item:
            if current_block:
                blocks.append(current_block)
            current_block = line
            continue

        # Jika baris adalah lanjutan kalimat sebelumnya
        if current_block:
            current_block += " " + line
        else:
            current_block = line

    if current_block:
        blocks.append(current_block)

    return "\n".join(blocks)


def clean_file(file_path: Path):
    if not file_path.exists():
        print(f"File tidak ditemukan: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    if isinstance(data, list):
        for item in data:
            if "content" in item:
                original = item["content"]
                cleaned = clean_legal_text(original)
                if cleaned != original:
                    item["content"] = cleaned
                    count += 1
    elif isinstance(data, dict):
        if "units" in data:
            for item in data["units"]:
                if "content" in item:
                    original = item["content"]
                    cleaned = clean_legal_text(original)
                    if cleaned != original:
                        item["content"] = cleaned
                        count += 1

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Berhasil merapikan {count} unit pada: {file_path.name}")


if __name__ == "__main__":
    print("Memulai pembersihan dan penataan format kutipan ayat...")
    clean_file(CHUNKS_PATH)
    clean_file(FAISS_META_PATH)
    clean_file(STRUCTURED_PATH)
    print("Selesai! Seluruh data chunk telah bersih dan rapi.")
