from functools import lru_cache
from src.config import get_settings
from langchain_core.retrievers import BaseRetriever
from src.vectordb.vector_store import get_vector_store

@lru_cache(maxsize=1)
def get_retriever() -> BaseRetriever:
    settings = get_settings()
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type= "similarity",
        search_kwargs= {
            "k": settings.retrieval_k
        }
    )