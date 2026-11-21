from langchain_huggingface import HuggingFaceEmbeddings
from src.core import config

settings = config.get_settings()

def embeddings() -> HuggingFaceEmbeddings:
    """
    Create and return a HuggingFaceEmbeddings instance using the specified embedding model.
    
    Returns:
        HuggingFaceEmbeddings: An instance of HuggingFaceEmbeddings initialized with the specified model.
    """
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
        )