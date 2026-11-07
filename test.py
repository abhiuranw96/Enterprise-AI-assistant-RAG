from src.config import get_settings
from src.llm.chat_model import get_chat_model
settings = get_settings()
print("App: ", settings.app_name)
print("Pinecone index: ", settings.pinecone_index_name)
print("Pinecone key configured: ", settings.pinecone_api_key is not None)

print("Ollama base URL: ", settings.ollama_base_url)

chat_model = get_chat_model()
print("Chat model: ", chat_model.model)