from typing import TypedDict
from langchain_core.documents import Document

class RAGState(TypedDict, total=False):
    """
    Represents the state of the RAG (Retrieval-Augmented Generation) process.
    """
    input: str
    search_query: str
    documents: list[Document]
    retrieval_grade: str
    answer_grade: str
    answer: str
    source_page: list[int]
    retry_count: int
    