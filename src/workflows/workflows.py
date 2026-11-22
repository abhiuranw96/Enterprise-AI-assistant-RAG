from typing import Literal
from langgraph.graph import END, START, StateGraph
from src.state.state import AgentState, QueryRouter, GradeEvidence
from src.generation.generate import generate_from_kb, generate_from_web, direct_ans, insufficient_ans
from src.llm.model import llm, web_search_tool
from src.retrieval import retrieve

# Node 1: Route -> KB or Direct
router_llm = llm.with_structured_output(QueryRouter, method="json_mode")

def decision_router(query: AgentState):
    question = query["question"]
    
    decision = router_llm.invoke(f'''
    You are a router for an Agentic RAG system. You will be given a question and you need to decide whether to use the knowledge base (KB) for answer or direct from web search.
    Route to "kb" if the user ask the question about:
    - agentic rag
    - agentic rag architecture
    - agentic rag components
    - agentic rag workflow
    - retrieval grading
    - rewriting the answer based on retrieved documents
    - retriever tools
    - web fallback in rag
    
    Route to "direct" only for the greeting or general questions.
    
    Question: {query["question"]}
    
    Return answer as a valid JSON object with the following format:
    {{
        "route": "kb" or "direct"
    }}
    
    ''')
    
    print("[Route]: ", decision.route)
    
    return {
        "current_query": question,
        "source": decision.route
    }
    

def route_after_router(state: AgentState) -> Literal["retrieve_kb", "direct_ans"]:
    if state["source"] == "kb":
        return "retrieve_kb"
    else:
        return "direct_ans"


# Node 2 -> KB retriever (retrieve_kb)

def retrieve_kb(state: AgentState) -> AgentState:
    query = state["current_query"]
    
    docs = retrieve(query)
    
    print("[Retrieved query]: ", query)
    print("[Retrieved docs]: ", len(docs))
    
    return {
        
        "kb_docs": docs
    }
    
# Node 3 -> Grade KB (grade_kb)
grade_llm = llm.with_structured_output(GradeEvidence, method="json_mode")

def grade_kb(state: AgentState) -> AgentState:
    question = state["question"]
    context = "\n\n".join(
        f"Source: {doc.metadata.get('source')}\nContent: {doc.page_content}"
        for doc in state["kb_docs"]
    )
    grade = grade_llm.invoke(f'''
    You are a private kb evidence grading agent for an Agentic RAG system. 
    You will be given a question and the retrieved documents from the 
    knowledge base (KB). You need to grade the retrieved documents as "good" or "weak" evidence for the question.
    
    question: {question}
    private_kb_evidence: {context}
                                
                                
                                
    return answer as a valid JSON object with the following format:
    {{
        "grade": "good" or "weak"
    }}
    
''')
    
    print("kb grading: ",grade.grade)
    
    return {
        "grade_kb": grade.grade
    }
    
def route_after_kb_grading(state: AgentState) -> Literal["generate_from_kb", "web_search"]:
    if state["grade_kb"] == "good":
        return "generate_from_kb"
    else:
        return "web_search"
    

# Node 4 ->  Tavily web search fallback
def web_search(state: AgentState) -> AgentState:
    question = state["current_query"]
    results = web_search_tool.invoke(question)
    
    # tavily may return dict/list of dict, we need to convert it to list of Document
    if isinstance(results, dict):
        answer = results.get("answer", "")
        result = results.get("results", [])
        lines = []
        
        if answer:
            lines.append(f"Tavily answer: {answer}")
            
        for item in result:
            title = item.get("title", "")
            url = item.get("url", "")
            content = item.get("content", "")
            lines.append(f"Title: {title}, URL: {url}, Content: {content}")
            
        web_ans = "\n\n".join(lines) if lines else str(results)
    else:
        web_ans = str(results)
        
    print("[Web search answer] characters: ", len(web_ans))
    
    return {
        "web_results": web_ans,
        "source": "web",
    }
    
    
# Node 5 -> Grade Web result

grade_web_llm = llm.with_structured_output(GradeEvidence, method="json_mode")
def grade_web(state: AgentState) -> AgentState:
    question = state["current_query"]
    web_ans = state["web_results"]
    
    grade = grade_web_llm.invoke(f'''
        You are a web evidence grading agent for an Agentic RAG system. 
        You will be given a question and the retrieved documents from the 
        web search (TavilySearch). You need to grade the retrieved documents as "good" or "weak" evidence for the question.
        
        question: {question}
        web_search_evidence: {web_ans}
                                    
                                    
                                    
        return answer as a valid JSON object with the following format:
        {{
            "grade": "good" or "weak"
        }}
        
    ''')
    
    print("web grading: ",grade.grade)
    
    return {
        "grade_web": grade.grade
    }

max_retries = 1
def route_after_web_grading(state: AgentState) -> Literal["generate_from_web", "rewrite_query","insufficient_ans"]:
    if state["grade_web"] == "good":
        return "generate_from_web"
    elif state["retry_count"] < max_retries:
        return "rewrite_query"
    else:
        return "insufficient_ans"
    
    
    
# Node 6 -> Rewrite query for web search
def rewrite_query(state: AgentState) -> AgentState:
    question = state["current_query"]
    retry_count = state["retry_count"] + 1
    
    rewritten = llm.invoke(f'''
Rewrite the question for better retrieval and web search.

Rules:
- Preserve original intent.
- Make it specific and search-friendly.
- Do not answer.
- Return only the rewritten query.

Original question:
{question}
''').content.strip()
    
    print("rewritten query: ",rewritten)
    
    return {
        "current_query": rewritten,
        "retry_count": retry_count,
    }

    
    
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("decision_router", decision_router)
    workflow.add_node("retrieve_kb", retrieve_kb)
    workflow.add_node("grade_kb", grade_kb)
    workflow.add_node("web_search", web_search)
    workflow.add_node("grade_web", grade_web)
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("generate_from_kb", generate_from_kb)
    workflow.add_node("generate_from_web", generate_from_web)
    workflow.add_node("direct_ans", direct_ans)
    workflow.add_node("insufficient_ans", insufficient_ans)

# Define the edges between nodes
    workflow.add_edge(START, "decision_router")
    workflow.add_conditional_edges(
    "decision_router", 
    route_after_router, 
    {
        "kb": "retrieve_kb",
        "direct": "direct_ans"
    }
)
    workflow.add_edge("retrieve_kb", "grade_kb")
    workflow.add_conditional_edges(
    "grade_kb", 
    route_after_kb_grading, 
    {
        "good": "generate_from_kb",
        "weak": "web_search"
    }
)

    workflow.add_edge("web_search", "grade_web")
    workflow.add_conditional_edges(
    "grade_web", 
    route_after_web_grading, 
    {
        "good": "generate_from_web",
        "weak": "rewrite_query",
        "insufficient": "insufficient_ans"
    }
)

    workflow.add_edge("rewrite_query", "retrieve_kb")
    workflow.add_edge("generate_from_kb", END)
    workflow.add_edge("generate_from_web", END)
    workflow.add_edge("direct_ans", END)
    workflow.add_edge("insufficient_ans", END)

    return workflow.compile()

agent_graph = build_graph()
    