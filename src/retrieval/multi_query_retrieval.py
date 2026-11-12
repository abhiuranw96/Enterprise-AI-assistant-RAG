from functools import lru_cache
from src.llm.chat_model import get_chat_model
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from src.retrieval.base_retrieval import base_retriever

@lru_cache(maxsize=1)
def get_multi_query_retriever() -> MultiQueryRetriever:
    chat_model = get_chat_model()
    return MultiQueryRetriever(
        retriever = base_retriever(),
        llm=chat_model,
        include_original=True
    )
