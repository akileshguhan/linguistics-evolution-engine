from services.embeddings import get_embedding

print("Testing get_embedding('the huns invade')...")
try:
    vec = get_embedding("the huns invade")
    print(f"Norm: {len(vec)} dimensions. First 5: {vec[:5]}")
except Exception as e:
    print(f"Error: {e}")
