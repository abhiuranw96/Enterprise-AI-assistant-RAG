from functools import lru_cache
from src.config import get_settings
from langchain_pinecone import PineconeVectorStore
from src.embeddings.embeddings import get_ollama_embeddings

@lru_cache(maxsize=1)
def get_vector_store() -> PineconeVectorStore:
    settings = get_settings()
    
    if settings.pinecone_api_key is None:
        raise ValueError("Pinecone API key is not configured in settings.")
    
    return PineconeVectorStore(
        api_key=settings.pinecone_api_key.get_secret_value(),
        index_name=settings.pinecone_index_name,
        namespace=settings.pinecone_namespace,
        embedding = get_ollama_embeddings()
    )