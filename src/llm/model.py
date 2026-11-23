from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from src.core import config
import logging

logger = logging.getLogger(__name__)
settings = config.get_settings()

_llm=None
_web_search = None

def get_llm() -> ChatGroq:
    global _llm
    if _llm is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is missing")
        _llm = ChatGroq(
            model=settings.chat_model,
            temperature=0,
            api_key=settings.groq_api_key,
        )
    return _llm

def get_web_search_tool():
    global _web_search
    if _web_search is None:
        if not settings.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY is missing")
        _web_search = TavilySearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=5,
            topic="general",
            include_answer=True,
            include_raw_content=False,
        )
    return _web_search


llm = get_llm()
web_search_tool = get_web_search_tool()
    
