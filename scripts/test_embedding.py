import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("NINEROUTER_BASE_URL")
API_KEY = os.getenv("NINEROUTER_API_KEY")
MODEL = os.getenv("EMBEDDING_MODEL")

url = f"{BASE_URL.rstrip('/')}/v1/embeddings"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL,
    "input": ["Ini adalah pengujian embedding untuk GITA."]
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60
)

print("Status:", response.status_code)

print("Response:", response.text)

response.raise_for_status()

result = response.json()
embedding = result["data"][0]["embedding"]

print("Embedding berhasil dibuat!")
print("Dimensi:", len(embedding))
print("Contoh nilai:", embedding[:5])