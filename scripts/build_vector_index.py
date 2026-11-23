"""
Skrip Pembuatan Indeks Vektor (Vector Knowledge Base)
GITA - Gerbang Informasi Tata Gereja Toraja

Fungsi:
1. Membaca 158 chunk dari data/processed/chunks.json.
2. Mengirimkan teks ke model embedding (gemini-embedding-001 via 9Router) secara batch.
3. Melakukan normalisasi L2 pada vektor (Exact Cosine Similarity).
4. Menyimpan matriks vektor (vectors.npy) dan metadata mapping (faiss_metadata.json).
5. Kompatibel ganda: Menggunakan FAISS jika tersedia, dan otomatis memakai NumPy exact FlatIP.
"""

import os
import json
import time
import requests
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BASE_URL = os.getenv("NINEROUTER_BASE_URL", "http://localhost:20128").rstrip("/")
API_KEY = os.getenv("NINEROUTER_API_KEY", "")
MODEL = os.getenv("EMBEDDING_MODEL", "gemini/gemini-embedding-001")

CHUNKS_FILE = BASE_DIR / "data" / "processed" / "chunks.json"
VECTORS_FILE = BASE_DIR / "data" / "processed" / "vectors.npy"
METADATA_FILE = BASE_DIR / "data" / "processed" / "faiss_metadata.json"
FAISS_INDEX_FILE = BASE_DIR / "data" / "processed" / "faiss_index.bin"

BATCH_SIZE = 10


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Memanggil endpoint embedding untuk sekumpulan teks (batch)."""
    url = f"{BASE_URL}/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "input": texts
    }

    response = requests.post(url, headers=headers, json=payload, timeout=90)
    response.raise_for_status()

    res_json = response.json()
    data = res_json.get("data", [])
    data_sorted = sorted(data, key=lambda x: x["index"])
    return [item["embedding"] for item in data_sorted]


def normalize_l2(arr: np.ndarray) -> np.ndarray:
    """Melakukan normalisasi L2 agar perkalian dot bernilai persis Cosine Similarity [-1.0 .. 1.0]."""
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return arr / norms


def build_vector_index():
    if not CHUNKS_FILE.exists():
        print(f"[ERROR] File chunks tidak ditemukan: {CHUNKS_FILE}")
        return False

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    total_chunks = len(chunks)
    print(f"\n=======================================================")
    print(f" Membangun Indeks Vektor Knowledge Base untuk GITA")
    print(f" Total Chunk  : {total_chunks}")
    print(f" Model        : {MODEL}")
    print(f" AI Gateway   : {BASE_URL}")
    print(f"=======================================================\n")

    all_embeddings = []
    metadata_list = []

    print("[1/3] Meng-generate embedding vektor dari teks chunk...")
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        texts = [chunk["content"] for chunk in batch_chunks]

        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE

        print(f"      Batch {batch_num}/{total_batches} (Chunk {i + 1} - {min(i + BATCH_SIZE, total_chunks)})...", end="", flush=True)

        try:
            embeddings = get_embeddings_batch(texts)
            all_embeddings.extend(embeddings)

            for chunk in batch_chunks:
                metadata_list.append({
                    "chunk_id": chunk["chunk_id"],
                    "document": chunk["document"],
                    "source": chunk["source"],
                    "type": chunk["type"],
                    "section": chunk["section"],
                    "chapter": chunk["chapter"],
                    "article": chunk["article"],
                    "page_start": chunk["page_start"],
                    "page_end": chunk["page_end"],
                    "content": chunk["content"]
                })

            print(" [OK]")
            time.sleep(0.3)
        except Exception as e:
            print(f" [GAGAL]\n[ERROR] Gagal pada batch {batch_num}: {e}")
            return False

    # Konversi ke NumPy array float32 & normalisasi L2
    print("\n[2/3] Membangun representasi matriks vektor (Cosine Similarity)...")
    embeddings_np = np.array(all_embeddings, dtype=np.float32)
    normalized_vectors = normalize_l2(embeddings_np)
    dimension = normalized_vectors.shape[1]
    print(f"      -> Dimensi vektor   : {dimension}")
    print(f"      -> Total vektor     : {len(normalized_vectors)}")

    # Coba simpan ke FAISS jika modul faiss tersedia di sistem
    faiss_saved = False
    try:
        import faiss
        index = faiss.IndexFlatIP(dimension)
        index.add(normalized_vectors)
        faiss.write_index(index, str(FAISS_INDEX_FILE))
        faiss_saved = True
        print(f"      -> FAISS Index      : Berhasil disimpan ({FAISS_INDEX_FILE.name})")
    except Exception as e:
        print(f"      -> FAISS Index      : Menggunakan NumPy FlatIP Engine (Sistem aman, no DLL issue)")

    # Simpan Matriks Vektor NumPy & Metadata
    print("\n[3/3] Menyimpan vektor & metadata...")
    np.save(VECTORS_FILE, normalized_vectors)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)

    print("\n-------------------------------------------------------")
    print(f" [SUKSES] Knowledge Base Vektor berhasil dibangun!")
    print(f" Matriks Vektor    : {VECTORS_FILE}")
    print(f" Metadata Mapping  : {METADATA_FILE}")
    print(f" Total Vektor      : {len(normalized_vectors)}")
    print(f" Ukuran Matriks    : {normalized_vectors.shape}")
    print(f"-------------------------------------------------------\n")
    return True


if __name__ == "__main__":
    build_vector_index()
