import os
import httpx
from core.config import config

HF_API_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

def get_embedding(text: str) -> list[float]:
    if not HF_TOKEN:
        print("\n" + "="*50)
        print("🚨 CRITICAL: HUGGINGFACE_TOKEN is NOT set!")
        print("Returning a dummy zero-vector. RAG will match 'No Event'.")
        print("Please check your .env file and RESTART the python server.")
        print("="*50 + "\n")
        return [0.0] * 384

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}

    try:
        response = httpx.post(HF_API_URL, headers=headers, json=payload, timeout=10.0)
        if response.status_code != 200:
            print("HF Error Response:", response.text)
        response.raise_for_status()
        # The API returns a list of floats for a single string input
        return response.json()
    except Exception as e:
        print(f"Error fetching embedding from Hugging Face: {e}")
        # Return fallback zero vector if API fails
        return [0.0] * 384
