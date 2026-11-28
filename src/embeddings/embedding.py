from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.core import config

settings = config.get_settings()

def embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Create and return a GoogleGenerativeAIEmbeddings instance using the specified embedding model.
    
    Returns:
        GoogleGenerativeAIEmbeddings: An instance of GoogleGenerativeAIEmbeddings initialized with the specified model.
    """
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
        output_dimensionality=384,
        )