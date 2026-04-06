from __future__ import annotations
from typing import Sequence
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import K_REL_CHUNKS, MODEL_NAME_RETR

def retrieve_relevant_chunks(question: str, chunks: Sequence[str]) -> list[str]:
    if not question or not question.strip():
        raise ValueError("Ошибка: пустой вопрос")
    if not chunks:
        return []

    clean_chunks = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not clean_chunks:
        return []

    model = SentenceTransformer(MODEL_NAME_RETR)

    chunk_embeddings = model.encode(clean_chunks, normalize_embeddings=True, convert_to_numpy=True)
    question_embedding = model.encode([question], normalize_embeddings=True, convert_to_numpy=True)

    chunk_embeddings = np.asarray(chunk_embeddings, dtype="float32")
    question_embedding = np.asarray(question_embedding, dtype="float32")

    index = faiss.IndexFlatIP(chunk_embeddings.shape[1])
    index.add(chunk_embeddings)

    top_k = min(K_REL_CHUNKS, len(clean_chunks))
    scores, indices = index.search(question_embedding, top_k)

    return [
        clean_chunks[idx]
        for score, idx in zip(scores[0], indices[0])
        if idx != -1 and score > 0
    ]
