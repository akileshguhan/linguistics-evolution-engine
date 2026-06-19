import os
import numpy as np
from supabase import create_client, Client
from core.config import config

def get_supabase() -> Client:
    url: str = config.SUPABASE_URL
    key: str = config.SUPABASE_KEY
    if url and key:
        return create_client(url, key)
    return None

supabase: Client = get_supabase()

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

def search_closest_event(embedding_vector: list[float]):
    if not supabase:
        return None
    try:
        # Fetch all events (there are only ~20, so this is extremely fast and avoids needing a Supabase RPC)
        response = supabase.table('historical_events').select('*').execute()
        events = response.data
        
        if not events:
            return None
            
        target_vec = np.array(embedding_vector)
        best_match = None
        best_score = -1.0
        
        for event in events:
            # pgvector returns embedding as a list/string depending on postgrest, we parse it
            import json
            vec_str = event.get('embedding')
            if isinstance(vec_str, str):
                vec = np.array(json.loads(vec_str))
            else:
                vec = np.array(vec_str)
                
            score = cosine_similarity(target_vec, vec)
            if score > best_score:
                best_score = score
                best_match = event
                
        return best_match
    except Exception as e:
        print(f"Supabase search error: {e}")
        return None
