"""
build_index.py
--------------
Generates embeddings for the unified knowledge base and upserts them
into a Pinecone vector index.

Usage:
    python build_index.py
"""

import json
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from data_loader import load_all_data
from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
)


def build():
    # 1. Load data
    print("Loading data...")
    df = load_all_data()
    print(f"  → {len(df)} records loaded.")

    # 2. Generate embeddings
    print(f"Generating embeddings with {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    descriptions = df["description"].tolist()
    embeddings = model.encode(descriptions, show_progress_bar=False, batch_size=32)

    # 3. Connect to Pinecone
    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Create index if it doesn't exist
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(PINECONE_INDEX_NAME)

    # 4. Upsert vectors in batches
    print("Upserting vectors...")
    batch_size = 50
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]

        vectors = []
        for j, (_, row) in enumerate(batch_df.iterrows()):
            vectors.append({
                "id": row["id"],
                "values": batch_embeddings[j].tolist(),
                "metadata": {
                    "title": row["title"],
                    "description": row["description"],
                    "industry": row["industry"],
                    "source": row["source"],
                },
            })

        index.upsert(vectors=vectors)

    print(f"Done! Upserted {len(df)} vectors into '{PINECONE_INDEX_NAME}'.")
    print(f"Index stats: {index.describe_index_stats()}")


if __name__ == "__main__":
    build()
