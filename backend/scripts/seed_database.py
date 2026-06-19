import os
import sys

# Add parent directory to path so we can import core/services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.embeddings import get_embedding
from services.supabase_client import supabase

if not supabase:
    print("Supabase client not configured. Check .env")
    sys.exit(1)

EVENTS = [
    {
        "event_key": "none",
        "name": "No Major Historical Event",
        "description": "Language drifts naturally without external shock events.",
        "vector_offsets": [0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "event_key": "highland_isolation",
        "name": "Highland Isolation",
        "description": "Tribes isolated in high mountain ranges. Air is thin. Consonants shift toward the back of the mouth (velarization); vowels shorten due to high-altitude respiration.",
        "vector_offsets": [0.2, -0.1, -0.1, -0.2, 0.2]
    },
    {
        "event_key": "nomadic_conquest",
        "name": "Nomadic Conquest",
        "description": "Violent horseback nomadic invasion (e.g. Kurgan expansion). Increases plosive and forceful breath sounds while dropping voicing consistency under rapid language assimilation.",
        "vector_offsets": [0.0, 0.3, -0.2, 0.1, -0.1]
    },
    {
        "event_key": "trade_integration",
        "name": "Maritime Trade Integration",
        "description": "Coastal trade creates a melting pot. Complex manners of articulation simplify into fricatives and approximants; voicing increases to ease cross-cultural communication.",
        "vector_offsets": [-0.1, -0.2, 0.2, 0.0, 0.0]
    },
    {
        "event_key": "grimms_law",
        "name": "Systematic Consonant Shift (Grimm's Law)",
        "description": "A natural generational systematic shift where voiced stops become voiceless stops, and voiceless stops shift into fricatives systematically.",
        "vector_offsets": [0.1, -0.3, -0.4, 0.0, 0.0]
    },
    {
        "event_key": "volcanic_winter",
        "name": "Volcanic Winter & Famine",
        "description": "A massive volcanic eruption blocks the sun, causing famine. Language becomes hushed, energy-conserving, vowels become closed and consonants nasalized.",
        "vector_offsets": [0.0, -0.2, 0.3, 0.4, 0.0]
    },
    {
        "event_key": "deep_forest",
        "name": "Deep Forest Isolation",
        "description": "Migration into dense jungles. Acoustic transmission favors loud, open vowels and highly distinct places of articulation to cut through foliage noise.",
        "vector_offsets": [0.3, 0.0, 0.1, -0.4, -0.2]
    },
    {
        "event_key": "imperial_assimilation",
        "name": "Imperial Assimilation",
        "description": "A massive centralized empire enforces standardized education and bureaucracy. Erratic local accents are smoothed out, increasing vowel centrality and neutral voicing.",
        "vector_offsets": [-0.1, -0.1, 0.1, 0.1, -0.1]
    },
    {
        "event_key": "desertification",
        "name": "Desertification & Drought",
        "description": "Rivers dry up, causing migration across arid deserts. Dust and dry air lead to closed mouths, increased fricatives, and lowered vowel height.",
        "vector_offsets": [0.1, 0.2, -0.1, 0.3, 0.1]
    },
    {
        "event_key": "island_colonization",
        "name": "Island Colonization",
        "description": "Seafaring tribes colonize remote archipelagos. Language simplifies rapidly, losing complex consonant clusters, heavily favoring open vowels and simplified places of articulation.",
        "vector_offsets": [-0.2, -0.3, 0.2, -0.3, 0.2]
    }
]

def seed():
    print("Starting database seeding...")
    # Clear existing events
    supabase.table('historical_events').delete().neq('id', 0).execute()
    
    for event in EVENTS:
        print(f"Generating embedding for {event['name']}...")
        embedding = get_embedding(event['description'])
        
        data = {
            "event_key": event["event_key"],
            "name": event["name"],
            "description": event["description"],
            "vector_offsets": event["vector_offsets"],
            "embedding": embedding
        }
        
        supabase.table('historical_events').insert(data).execute()
        print(f"Inserted {event['name']}.")
        
    print("Database seeding complete!")

if __name__ == "__main__":
    seed()
