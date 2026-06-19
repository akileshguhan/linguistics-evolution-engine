import os
import certifi

# Force Python to use the updated certificate authority bundle
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from engine.phonetics import text_to_vectors, vectors_to_text
from engine.drift import evolve_word_vectors
from services.neo4j_client import Neo4jClient

app = FastAPI(title="Linguistic Evolution Engine API")

# Allow Next.js frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neo4j_db = Neo4jClient()

# --- Pydantic Models ---

class InitRequest(BaseModel):
    words: List[str]

class WordState(BaseModel):
    text: str
    epoch: int
    root_word: str

class AdvanceRequest(BaseModel):
    words: List[WordState]
    geography_isolation: float
    population_density: float
    literacy_rate: float
    climate_humidity: float
    custom_event_text: str

# Root endpoint for health checks (e.g. Render)
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Linguistic Evolution Engine API is running"}

# --- Endpoints ---

@app.post("/simulation/init")
async def initialize_simulation(payload: InitRequest):
    try:
        neo4j_db.clear_database()
        neo4j_db.initialize_proto_words(payload.words)
        
        # Return the structured state for the frontend to track
        initial_state = [{"text": w, "epoch": 0, "root_word": w} for w in payload.words]
        return {"status": "success", "active_words": initial_state}
    except Exception as e:
        print("\n🚨 CRASH REPORT 🚨")
        traceback.print_exc()  # This prints the exact reason for the crash
        print("🚨 END REPORT 🚨\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulation/advance")
async def advance_epoch(payload: AdvanceRequest):
    try:
        new_active_words = []

        for word_obj in payload.words:
            # 1. Encode text to vectors
            vectors = text_to_vectors(word_obj.text)
            
            # 2. Apply environmental and historical drift via RAG
            evolved_vectors, matched_event_name = evolve_word_vectors(
                proto_vectors=vectors,
                isolation=payload.geography_isolation,
                density=payload.population_density,
                literacy=payload.literacy_rate,
                climate=payload.climate_humidity,
                custom_event_text=payload.custom_event_text
            )
            
            # 3. Decode drifted vectors back to text
            new_text = vectors_to_text(evolved_vectors)
            
            # Update edge metadata with the matched RAG event name
            edge_metadata = {
                "event": matched_event_name,
                "isolation": payload.geography_isolation,
                "density": payload.population_density,
                "literacy": payload.literacy_rate,
                "climate": payload.climate_humidity
            }
            
            # 4. Save the evolutionary step in the Graph Database
            neo4j_db.create_mutation_step(
                parent_word=word_obj.text,
                parent_epoch=word_obj.epoch,
                child_word=new_text,
                root_word=word_obj.root_word,
                edge_metadata=edge_metadata
            )
            
            new_active_words.append({
                "text": new_text,
                "epoch": word_obj.epoch + 1,
                "root_word": word_obj.root_word
            })

        return {"status": "success", "active_words": new_active_words}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulation/tree")
async def get_phylogenetic_tree():
    try:
        tree_data = neo4j_db.get_complete_tree()
        return {"status": "success", "data": tree_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulation/state/{epoch_id}")
async def get_simulation_state(epoch_id: int):
    try:
        epoch_words = neo4j_db.get_epoch_state(epoch_id)
        return {"status": "success", "words": epoch_words}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))