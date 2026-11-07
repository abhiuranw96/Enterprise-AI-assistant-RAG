from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    app_name: str = "Enterprise AI knowledge System"
    app_env: str = "assistant_env"
    api_prefix: str = "/api/v1"
    
    # chat model
    chat_model : str = "llama3.2"
    
    # embedding model
    embedding_model: str = "nomic-embed-text"
    
    # Embeddings and vector database
    pinecone_api_key: SecretStr | None = None
    pinecone_index_name: str = "industry-agentic-rag"
    pinecone_namespace: str = "enterprise-ai-assistant"
    
    ollama_base_url: str = "http://localhost:11434"
    embedding_dimensions: int = 768
    
    # retrieval and graph
    retrieval_k: int = 8
    max_retrieval_retries: int = 1
    
    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        )
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()    
    
    
