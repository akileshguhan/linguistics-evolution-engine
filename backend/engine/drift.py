import numpy as np
from typing import List, Tuple

from services.embeddings import get_embedding
from services.supabase_client import search_closest_event

def calculate_environmental_vector(isolation: float, density: float, literacy: float, climate: float) -> np.array:
    """
    Translates continuous frontend slider variables into a raw 5D environmental drift offset.
    [place, manner, voicing, height, backness]
    """
    # Isolation: pushes sounds toward back of mouth (place) and decreases voicing stability
    isolation_effect = np.array([isolation * 0.15, 0.0, isolation * -0.1, 0.0, 0.0])
    
    # Density: drives vowel raising/shifting and forces articulation simplification
    density_effect = np.array([0.0, density * -0.1, density * 0.1, density * 0.2, 0.0])
    
    # Literacy (Standardization): Oral traditions mutate faster. Written standards centralize vowels and stabilize consonants.
    # High literacy (1.0) creates negative vectors to slow down drift (centralizing).
    literacy_effect = np.array([0.0, literacy * 0.1, literacy * 0.05, literacy * -0.15, literacy * -0.1])
    
    # Climate Humidity: Acoustic adaptation.
    # Hot/Humid (1.0) favors open vowels (height -) and tones (voicing +). Cold/Dry (0.0) favors consonants.
    climate_effect = np.array([climate * -0.1, climate * -0.15, climate * 0.2, climate * -0.2, 0.0])
    
    return isolation_effect + density_effect + literacy_effect + climate_effect

def evolve_word_vectors(proto_vectors: List[np.ndarray], isolation: float, density: float, literacy: float, climate: float, custom_event_text: str) -> Tuple[List[np.ndarray], str]:
    """
    Applies the mathematical evolutionary formula to an array of phonetic character vectors:
    V_evolved = V_proto + V_geography + V_history
    """
    matched_event_name = "Natural Drift"
    # 1. Fetch historical shift vector using RAG
    if custom_event_text and custom_event_text.strip():
        embedding = get_embedding(custom_event_text)
        best_match = search_closest_event(embedding)
        
        if best_match:
            matched_event_name = best_match.get('name')
            print(f"RAG matched event: {matched_event_name} for input: '{custom_event_text}'")
            history_vector = np.array(best_match.get('vector_offsets'))
        else:
            print("No matching event found, using zero vector.")
            history_vector = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    else:
        history_vector = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    
    # 2. Compute environmental baseline modifications
    geography_vector = calculate_environmental_vector(isolation, density, literacy, climate)
    
    # 3. Combine vectors to discover final mutation pressure
    total_pressure_vector = geography_vector + history_vector
    
    # 4. Mutate each character coordinate vector
    evolved_vectors = []
    for vec in proto_vectors:
        mutated_vec = vec + total_pressure_vector
        # Clamp results between 0.0 and 1.0 so features remain valid coordinates
        clamped_vec = np.clip(mutated_vec, 0.0, 1.0)
        evolved_vectors.append(clamped_vec)
        
    return evolved_vectors, matched_event_name