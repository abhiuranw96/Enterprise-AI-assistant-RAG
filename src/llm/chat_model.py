from functools import lru_cache
from langchain_ollama import ChatOllama
from src.config import get_settings

@lru_cache(maxsize=1)
def get_chat_model() -> ChatOllama:
    settings = get_settings()
    
    if settings.chat_model is None:
        raise ValueError("Chat model is not configured in settings.")
    
    return ChatOllama(
        model=settings.chat_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )