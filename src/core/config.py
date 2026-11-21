from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "Enterprise AI knowledge System"
    app_env: str = "assistant_env"
    api_prefix: str = "/api/v1"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # chat model
    chat_model: str = ""
    
    # embedding model
    embedding_model: str = ""
    
    # Embeddings and vector database
    pinecone_api_key: str = ""
    pinecone_index_name: str = "agentic-rag"
    pinecone_namespace: str = "IT-industry-agentic-rag"

    embedding_dimensions: int = 384
    
    # retrieval and graph
    retrieval_k: int = 4
    max_retries: int = 1
    admin_api_key: str = "abhi"
    audit_db_path: str = str(BASE_DIR / "data" / "audit.db")
    upload_dir: str = str(BASE_DIR / "uploads")
    sample_kb_dir: str = str(BASE_DIR / "data" / "sample_kb")
    
    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
