"""
FastAPI Backend Application for GITA (Gerbang Informasi Tata Gereja)
Kapita Selekta: AI Engineering - RAG Governance Assistant
"""

import os
import sys
import json
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
import requests
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Setup Base Path & Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("gita_backend")

# Import Modul Retrieval yang sudah kita buat
from scripts.retrieval import VectorRetriever

# Konfigurasi LLM & Gateway
BASE_URL = os.getenv("NINEROUTER_BASE_URL", "http://localhost:20128").rstrip("/")
API_KEY = os.getenv("NINEROUTER_API_KEY", "")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini/gemini-3.5-flash-lite")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini/gemini-embedding-001")

# Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="GITA API - Gerbang Informasi Tata Gereja",
    description="Backend RAG berbasis FastAPI, Gemini API, dan Vektor Knowledge Base",
    version="1.0.0"
)

# Konfigurasi CORS (Memungkinkan akses dari browser frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi Singleton Retriever
retriever_instance = None


def get_retriever() -> VectorRetriever:
    global retriever_instance
    if retriever_instance is None:
        try:
            logger.info("Memuat Vector Knowledge Base...")
            retriever_instance = VectorRetriever()
            total_loaded = len(retriever_instance.vectors) if retriever_instance.vectors is not None else 0
            logger.info(f"Knowledge Base siap dengan {total_loaded} chunk terindeks.")
        except Exception as e:
            logger.error(f"Gagal memuat Knowledge Base: {e}")
            raise RuntimeError(f"Gagal memuat Knowledge Base: {e}")
    return retriever_instance


# ==============================================================================
# Skema Data Request & Response (Pydantic Models)
# ==============================================================================
class QueryRequest(BaseModel):
    question: Optional[str] = Field(None, description="Teks pertanyaan pengguna (format frontend)")
    query: Optional[str] = Field(None, description="Teks pertanyaan alternatif")
    top_k: Optional[int] = Field(5, description="Jumlah maksimal chunk yang diambil", ge=1, le=10)
    threshold: Optional[float] = Field(0.75, description="Ambang batas kemiripan kosinus minimal", ge=0.0, le=1.0)

    @property
    def text(self) -> str:
        val = self.question or self.query or ""
        return val.strip()


class SourceItem(BaseModel):
    chunk_id: str
    document: str
    section: Optional[str] = None
    chapter: Optional[str] = None
    article: Optional[str] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    content: str
    similarity_score: Optional[float] = None


class QueryResponse(BaseModel):
    status: str = Field(..., description="Status respon: success, not_found, insufficient_evidence, error")
    answer: str = Field(..., description="Jawaban berbasis dokumen atau pesan penolakan yang jujur")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Daftar pasal rujukan yang mendasari jawaban")


# ==============================================================================
# Helper Pemanggilan LLM Gemini via 9Router
# ==============================================================================
SYSTEM_PROMPT = """Anda adalah GITA (Gerbang Informasi Tata Gereja), asisten AI resmi untuk menjawab ketentuan dan regulasi Gereja Toraja.
Tugas Anda: Menjawab pertanyaan pengguna secara akurat, lugas, dan berbobot HANYA berdasarkan naskah pasal resmi yang disediakan dalam KONTEKS RUJUKAN di bawah.

ATURAN WAJIB (STRICT GROUNDING & KESETIAAN PADA SUMBER):
1. Seluruh jawaban HANYA boleh bersumber dari teks pasal pada KONTEKS RUJUKAN. Dilarang keras berasumsi, mengarang ketentuan, atau menyelipkan pengetahuan umum di luar teks sumber.
2. Wajib mengutip nomor pasal dan ayat yang mendasari jawaban (contoh: 'Menurut Pasal 2 ayat (1)...' atau 'Sebagaimana diatur dalam Bab I Pasal 8...').
3. Format teks jawaban dalam format markdown dengan paragraf dan/atau poin-poin yang mudah dipahami, sopan, dan terstruktur rapi.
4. Jangan menyebut frasa teknis internal seperti 'berdasarkan potongan teks yang diberikan' atau 'dalam prompt di atas'. Gunakan frasa resmi: 'Berdasarkan naskah Tata Gereja Toraja...'.
5. Jika ada bagian dari pertanyaan yang tidak dibahas dalam pasal rujukan, nyatakan secara jujur dan tegas bahwa hal tersebut tidak diatur dalam pasal terkait.
"""


def generate_llm_answer(question: str, sources: List[Dict[str, Any]]) -> str:
    """Mengirim prompt grounding ke Gemini LLM dan mengambil teks jawaban."""
    context_blocks = []
    for i, s in enumerate(sources, start=1):
        pasal_info = f"Pasal {s.get('article')}" if s.get('article') else s.get('section')
        bab_info = f"BAB {s.get('chapter')} • " if s.get('chapter') else ""
        hlm_info = f"Halaman {s.get('page_start')}"
        context_blocks.append(
            f"--- [RUJUKAN {i}: {s['chunk_id']}] ({bab_info}{s.get('section', '')}, {pasal_info}, {hlm_info}) ---\n"
            f"{s['content']}"
        )

    context_str = "\n\n".join(context_blocks)
    user_message = f"KONTEKS RUJUKAN DARI TATA GEREJA TORAJA:\n\n{context_str}\n\nPERTANYAAN PENGURUS/PENGGUNA:\n{question}\n\nJAWABAN:"

    payload = {
        "model": CHAT_MODEL,
        "stream": False,
        "temperature": 0.1,  # Rendah agar jawaban faktual dan setia pada dokumen
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=40)
    response.raise_for_status()

    res_json = response.json()
    answer = res_json["choices"][0]["message"]["content"].strip()
    return answer


# ==============================================================================
# Endpoints
# ==============================================================================
@app.get("/")
def root():
    return {
        "status": "online",
        "app": "GITA - Gerbang Informasi Tata Gereja Backend API",
        "version": "1.0.0",
        "chat_model": CHAT_MODEL,
        "embedding_model": EMBEDDING_MODEL
    }


@app.get("/api/health")
def health_check():
    try:
        retriever = get_retriever()
        total_chunks = len(retriever.vectors) if retriever.vectors is not None else 0
        return {
            "status": "healthy",
            "knowledge_base_chunks": total_chunks,
            "gateway_status": "connected"
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/api/query", response_model=QueryResponse)
@app.post("/query", response_model=QueryResponse)
def handle_query(req: QueryRequest):
    """
    Endpoint utama RAG untuk memproses pertanyaan pengguna.
    Mengikuti alur: Validasi -> Semantic Search (FAISS) -> Grounded LLM Generation.
    """
    query_text = req.text
    if not query_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pertanyaan tidak boleh kosong."
        )

    logger.info(f"Menerima pertanyaan: '{query_text}'")

    try:
        retriever = get_retriever()
        # 1. Jalankan Semantic Retrieval
        retrieval_res = retriever.search(
            query=query_text,
            top_k=req.top_k or 5,
            threshold=req.threshold or 0.75
        )

        ret_status = retrieval_res["status"]
        highest_score = retrieval_res.get("highest_score", 0.0)

        # 2. Penanganan Kasus Penolakan (Sesuai Modul Dosen & Slide UTS)
        if ret_status == "not_found":
            logger.info(f"Ketentuan tidak ditemukan (skor tertinggi: {highest_score}).")
            return QueryResponse(
                status="not_found",
                answer="Ketentuan mengenai hal tersebut tidak ditemukan dalam naskah resmi Tata Gereja Toraja yang tersimpan dalam sistem.",
                sources=[]
            )

        if ret_status == "insufficient_evidence":
            logger.info(f"Bukti tidak mencukupi (skor tertinggi: {highest_score}).")
            return QueryResponse(
                status="insufficient_evidence",
                answer="Informasi atau ketentuan yang ditemukan dalam dokumen rujukan belum mencukupi untuk menjawab pertanyaan ini secara lengkap dan pasti.",
                sources=[]
            )

        # 3. Kasus Berhasil: Kirim Konteks ke Gemini AI
        sources = retrieval_res.get("sources", [])
        logger.info(f"Retrieval berhasil menemukan {len(sources)} rujukan (skor tertinggi: {highest_score}). Memanggil LLM...")

        answer = generate_llm_answer(query_text, sources)

        return QueryResponse(
            status="success",
            answer=answer,
            sources=sources
        )

    except requests.RequestException as re:
        logger.error(f"Gagal menghubungi model AI: {re}")
        return QueryResponse(
            status="error",
            answer="Terjadi kendala teknis saat berkomunikasi dengan layanan kecerdasan buatan. Silakan coba sesaat lagi.",
            sources=[]
        )
    except Exception as e:
        logger.error(f"Kesalahan internal pemrosesan: {e}")
        return QueryResponse(
            status="error",
            answer=f"Terjadi kesalahan dalam pemrosesan sistem: {str(e)}",
            sources=[]
        )


# Pasang antarmuka frontend agar dapat diakses langsung dari http://localhost:8000/app
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
