import json
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "processed" / "structured_document.json"

with open(INPUT_PATH, "r", encoding="utf-8") as file:
    document = json.load(file)

units = document["units"]

lengths = [
    len(unit["content"])
    for unit in units
]

print("ANALISIS PANJANG UNIT")
print("=" * 40)
print(f"Total unit       : {len(units)}")
print(f"Rata-rata        : {mean(lengths):.0f} karakter")
print(f"Terpendek        : {min(lengths)} karakter")
print(f"Terpanjang       : {max(lengths)} karakter")

print("\n10 UNIT TERPANJANG")
print("=" * 40)

longest_units = sorted(
    units,
    key=lambda unit: len(unit["content"]),
    reverse=True
)[:10]

for unit in longest_units:
    print(
        f"{unit['section']} | "
        f"Pasal {unit['article']} | "
        f"{len(unit['content'])} karakter"
    )