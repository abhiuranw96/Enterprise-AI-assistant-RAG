from langchain_huggingface import HuggingFaceEndpointEmbeddings
from src.core import config

settings = config.get_settings()

def embeddings() -> HuggingFaceEndpointEmbeddings:
    """
    Create and return a HuggingFaceEndpointEmbeddings instance using the specified embedding model.
    
    Returns:
        HuggingFaceEndpointEmbeddings: An instance of HuggingFaceEndpointEmbeddings initialized with the specified model.
    """
    return HuggingFaceEndpointEmbeddings(
        model=settings.embedding_model,
        task = "feature-extraction",
        huggingfacehub_api_token=settings.hf_token,
        )