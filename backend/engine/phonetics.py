import numpy as np
from typing import List

# 5D Phonetic Feature Vector Mapping:
# [place_of_articulation, manner_of_articulation, voicing, vowel_height, vowel_backness]
# Values range from 0.0 to 1.0 to map physical vocal tract coordinates.
PHONEME_REGISTRY = {
    # Consonants
    'p': np.array([0.1, 0.9, 0.0, 0.0, 0.0]),  # Bilabial, Plosive, Voiceless
    'b': np.array([0.1, 0.9, 1.0, 0.0, 0.0]),  # Bilabial, Plosive, Voiced
    'm': np.array([0.1, 0.7, 1.0, 0.0, 0.0]),  # Bilabial, Nasal, Voiced
    't': np.array([0.3, 0.9, 0.0, 0.0, 0.0]),  # Alveolar, Plosive, Voiceless
    'd': np.array([0.3, 0.9, 1.0, 0.0, 0.0]),  # Alveolar, Plosive, Voiced
    'n': np.array([0.3, 0.7, 1.0, 0.0, 0.0]),  # Alveolar, Nasal, Voiced
    's': np.array([0.3, 0.5, 0.0, 0.0, 0.0]),  # Alveolar, Fricative, Voiceless
    'z': np.array([0.3, 0.5, 1.0, 0.0, 0.0]),  # Alveolar, Fricative, Voiced
    'k': np.array([0.7, 0.9, 0.0, 0.0, 0.0]),  # Velar, Plosive, Voiceless
    'g': np.array([0.7, 0.9, 1.0, 0.0, 0.0]),  # Velar, Plosive, Voiced
    'f': np.array([0.2, 0.5, 0.0, 0.0, 0.0]),  # Labiodental, Fricative, Voiceless
    'v': np.array([0.2, 0.5, 1.0, 0.0, 0.0]),  # Labiodental, Fricative, Voiced
    'r': np.array([0.3, 0.3, 1.0, 0.0, 0.0]),  # Alveolar, Approximant, Voiced
    'l': np.array([0.3, 0.2, 1.0, 0.0, 0.0]),  # Alveolar, Lateral Approximant

    # Vowels (place/manner/voicing are zeroed or neutralized, height & backness active)
    'a': np.array([0.0, 0.0, 1.0, 0.1, 0.5]),  # Open, Central Vowel
    'e': np.array([0.0, 0.0, 1.0, 0.5, 0.2]),  # Close-Mid, Front Vowel
    'i': np.array([0.0, 0.0, 1.0, 0.9, 0.1]),  # Close, Front Vowel
    'o': np.array([0.0, 0.0, 1.0, 0.5, 0.8]),  # Close-Mid, Back Vowel
    'u': np.array([0.0, 0.0, 1.0, 0.9, 0.9]),  # Close, Back Vowel
}

def text_to_vectors(text: str) -> List[np.ndarray]:
    """
    Encodes a string of plain text characters into a sequence of 5D phonetic feature vectors.
    Characters not in the registry are quietly skipped to prevent runtime crashes.
    """
    vectors = []
    for char in text.lower():
        if char in PHONEME_REGISTRY:
            vectors.append(PHONEME_REGISTRY[char])
    return vectors

def vectors_to_text(vectors: List[np.ndarray]) -> str:
    """
    Decodes a sequence of drifted 5D vectors back into a printable text string
    using a Euclidean Nearest-Neighbor lookup metric.
    """
    decoded_chars = []
    
    for vec in vectors:
        closest_char = None
        min_distance = float('inf')
        
        for char, registry_vec in PHONEME_REGISTRY.items():
            # Calculate Euclidean distance between drifted point and known static phoneme coordinate
            distance = np.linalg.norm(vec - registry_vec)
            if distance < min_distance:
                min_distance = distance
                closest_char = char
                
        if closest_char:
            decoded_chars.append(closest_char)
            
    return "".join(decoded_chars)