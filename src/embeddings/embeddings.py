from functools import lru_cache
from src.config import get_settings
from langchain_ollama import OllamaEmbeddings

@lru_cache(maxsize=1)
def get_ollama_embeddings() -> OllamaEmbeddings:
    settings = get_settings()
    
    if settings.embedding_model is None:
        raise ValueError("Embedding model is not configured in settings.")
    
    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )
