from src.vectordb.vector_store import get_vectorstore
from src.core import config
settings = config.get_settings()

def get_retriever():
    return get_vectorstore().as_retriever(
        search_kwargs={
            "k": settings.retrieval_k
            }
        )