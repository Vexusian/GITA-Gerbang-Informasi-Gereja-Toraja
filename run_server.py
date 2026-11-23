"""
Runner Skrip untuk Menjalankan Backend FastAPI GITA
GITA - Gerbang Informasi Tata Gereja Toraja

Cara Menjalankan:
    python run_server.py

Akses:
    - Web Chat Interface: http://127.0.0.1:8000/app/index.html
    - Swagger API Docs  : http://127.0.0.1:8000/docs
    - API Endpoint      : http://127.0.0.1:8000/api/query
"""

import sys
from pathlib import Path
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" Memulai Server GITA Backend (FastAPI + Gemini RAG)")
    print("=" * 60)
    print(" -> Antarmuka Web Chat  : http://127.0.0.1:8000/app/index.html")
    print(" -> Dokumentasi Swagger : http://127.0.0.1:8000/docs")
    print(" -> Health Endpoint     : http://127.0.0.1:8000/api/health")
    print("=" * 60 + "\n")

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
