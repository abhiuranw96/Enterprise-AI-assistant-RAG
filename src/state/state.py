from typing import List, Literal, TypedDict
from pydantic import BaseModel, Field
from langchain_core.documents import Document

class QueryRouter(BaseModel):
    """
    It decides whether to use KB for answer or direct from web search
    """
    route: Literal["kb","direct"] = Field(
        description="Use kb for questions related to Agentic RAG docs, use direct for normal greet/chating or general questions"
    )
    
class GradeEvidence(BaseModel):
    """
    It grades the retrieved documents or answer as good or weak evidence for the query.
    """
    grade: Literal["good","weak"] = Field(
        description="Good evidence means the retrieved documents or answer is relevant to the query, weak evidence means the retrieved documents or answer is not relevant to the query"
    )

class AgentState(TypedDict):
    question: str
    current_query: str
    kb_docs: List[Document]
    web_results: str
    grade_kb: str
    grade_web: str
    answer: str
    source: str
    retry_count: int
    
