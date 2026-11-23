"""
Modul Retrieval & Semantic Search (Knowledge Base Search)
GITA - Gerbang Informasi Tata Gereja Toraja

Fungsi:
1. Menerima pertanyaan teks dari pengguna.
2. Mengubah pertanyaan menjadi vektor embedding (gemini-embedding-001).
3. Melakukan pencarian kemiripan kosinus (Cosine Similarity / FlatIP) terhadap seluruh vektor.
4. Menerapkan ambang batas kemiripan (Similarity Threshold: 0.75) dan batas Top-K (maks 5 chunk).
5. Mengembalikan hasil terstruktur (status: success / not_found / insufficient_evidence).
"""

import os
import sys
import json
import requests
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BASE_URL = os.getenv("NINEROUTER_BASE_URL", "http://localhost:20128").rstrip("/")
API_KEY = os.getenv("NINEROUTER_API_KEY", "")
MODEL = os.getenv("EMBEDDING_MODEL", "gemini/gemini-embedding-001")

VECTORS_FILE = BASE_DIR / "data" / "processed" / "vectors.npy"
METADATA_FILE = BASE_DIR / "data" / "processed" / "faiss_metadata.json"

DEFAULT_TOP_K = 5
DEFAULT_THRESHOLD = 0.75


class VectorRetriever:
    def __init__(self):
        self.vectors: np.ndarray = np.empty((0, 3072), dtype=np.float32)
        self.metadata: list[dict] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Memuat matriks vektor dan metadata ke memori."""
        if not VECTORS_FILE.exists() or not METADATA_FILE.exists():
            raise FileNotFoundError(
                f"Knowledge Base belum dibangun. Jalankan 'scripts/build_vector_index.py' terlebih dahulu."
            )

        self.vectors = np.load(VECTORS_FILE)  # shape: (N, 3072)
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        if len(self.vectors) != len(self.metadata):
            raise ValueError(
                f"Ukuran vektor ({len(self.vectors)}) dan metadata ({len(self.metadata)}) tidak cocok!"
            )

    def embed_query(self, query: str) -> np.ndarray:
        """Meng-generate embedding untuk kueri pertanyaan."""
        url = f"{BASE_URL}/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "input": [query.strip()]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        embedding = response.json()["data"][0]["embedding"]
        vec = np.array(embedding, dtype=np.float32).reshape(1, -1)

        # L2-normalize agar dot product bernilai tepat Cosine Similarity
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def search(self, query: str, top_k: int = DEFAULT_TOP_K, threshold: float = DEFAULT_THRESHOLD) -> dict:
        """
        Menjalankan semantic similarity search terhadap seluruh dokumen rujukan.
        """
        if not query or not query.strip():
            return {
                "status": "error",
                "message": "Kueri pertanyaan tidak boleh kosong.",
                "sources": []
            }

        # 1. Ubah pertanyaan menjadi vektor
        query_vec = self.embed_query(query)

        # 2. Hitung Cosine Similarity melalui Dot Product matriks (1, D) @ (D, N) -> (N,)
        scores = np.dot(self.vectors, query_vec.T).flatten()

        # 3. Urutkan dari skor kemiripan tertinggi ke terendah
        sorted_indices = np.argsort(scores)[::-1]

        # Ambil top candidate
        candidates = []
        highest_score = float(scores[sorted_indices[0]]) if len(sorted_indices) > 0 else 0.0

        for idx in sorted_indices[:top_k]:
            score = float(scores[idx])
            meta = self.metadata[idx]

            candidates.append({
                "chunk_id": meta["chunk_id"],
                "document": meta["document"],
                "section": meta["section"],
                "chapter": meta["chapter"],
                "article": meta["article"],
                "page_start": meta["page_start"],
                "page_end": meta["page_end"],
                "content": meta["content"],
                "similarity_score": round(score, 4)
            })

        # 4. Filter berdasarkan Threshold
        matched_sources = [c for c in candidates if c["similarity_score"] >= threshold]

        # 5. Tentukan Status Berdasarkan Bukti
        if len(matched_sources) > 0:
            status = "success"
        elif highest_score >= (threshold - 0.10):  # Mendekati batas (misal 0.65 - 0.74)
            status = "insufficient_evidence"
        else:
            status = "not_found"

        return {
            "status": status,
            "query": query,
            "highest_score": round(highest_score, 4),
            "threshold": threshold,
            "total_found": len(matched_sources),
            "sources": matched_sources if status == "success" else []
        }


def main():
    if len(sys.argv) < 2:
        test_query = "Apa hakikat dan wujud Gereja Toraja menurut Pasal 2?"
    else:
        test_query = " ".join(sys.argv[1:])

    print(f"\n=======================================================")
    print(f" Uji Coba Semantic Search (Retrieval Engine)")
    print(f" Pertanyaan : \"{test_query}\"")
    print(f" Threshold  : {DEFAULT_THRESHOLD}")
    print(f" Top-K      : {DEFAULT_TOP_K}")
    print(f"=======================================================\n")

    try:
        retriever = VectorRetriever()
        print(f"Total Dokumen di Knowledge Base: {len(retriever.vectors)} chunk")
        print("Mencari chunk paling relevan...")

        result = retriever.search(test_query)

        print(f"\nStatus Hasil        : {result['status'].upper()}")
        print(f"Skor Tertinggi      : {result['highest_score']}")
        print(f"Jumlah Rujukan Lolos: {result['total_found']}")

        if result["status"] == "success":
            print("\n[DAFTAR RUJUKAN TERVERIFIKASI]:")
            for i, src in enumerate(result["sources"], start=1):
                article = f"Pasal {src['article']}" if src['article'] else src['section']
                chapter = f"BAB {src['chapter']} • " if src['chapter'] else ""
                print(f"\n{i}. [{src['chunk_id']}] (Skor: {src['similarity_score']})")
                print(f"   Lokasi : {chapter}{src['section']} (Hlm. {src['page_start']})")
                print(f"   Teks   : {src['content'][:140]}...")
        elif result["status"] == "insufficient_evidence":
            print("\n[PENOLAKAN]: Bukti tidak mencukupi (Skor di bawah threshold 0.75).")
        else:
            print("\n[PENOLAKAN]: Ketentuan tidak ditemukan dalam dokumen resmi.")

        print("\n-------------------------------------------------------\n")
    except Exception as e:
        print(f"[ERROR]: {e}")


if __name__ == "__main__":
    main()
