
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "processed" / "structured_document.json"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "chunks.json"


def generate_chunk_id(unit):
    section_codes = {
        "Pembukaan": "PB",
        "Batang Tubuh": "BT",
        "Memori Penjelasan": "MP",
        "Lampiran 2": "L2"
    }

    section_code = section_codes[unit["section"]]
    article = unit["article"]
    chapter = unit["chapter"]

    if unit["type"] == "section":
        return f"TGT-{section_code}"

    if chapter:
        return (
            f"TGT-{section_code}-"
            f"BAB-{chapter}-PASAL-{article}"
        )

    return f"TGT-{section_code}-PASAL-{article}"


def create_chunks():
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        document = json.load(file)

    chunks = []

    for unit in document["units"]:
        content = unit["content"].strip()

        if not content:
            continue

        chunk = {
            "chunk_id": generate_chunk_id(unit),
            "document": document["document_title"],
            "source": document["source_file"],
            "type": unit["type"],
            "section": unit["section"],
            "chapter": unit["chapter"],
            "article": unit["article"],
            "page_start": unit["page_start"],
            "page_end": unit["page_end"],
            "content": content
        }

        chunks.append(chunk)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("Chunking selesai!")
    print(f"Total chunk: {len(chunks)}")
    print(f"Output: {OUTPUT_PATH}")

    # Periksa ID duplikat.
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    duplicates = [
        chunk_id
        for chunk_id in set(chunk_ids)
        if chunk_ids.count(chunk_id) > 1
    ]

    if duplicates:
        print(f"ID duplikat: {duplicates}")
    else:
        print("ID duplikat: Tidak ada")


if __name__ == "__main__":
    create_chunks()
