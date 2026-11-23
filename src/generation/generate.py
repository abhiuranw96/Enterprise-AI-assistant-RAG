from src.state.state import AgentState
from src.llm.model import llm

# Node 7 -> generate answer from KB
def generate_from_kb(state: AgentState) -> AgentState:
    question = state["current_query"]
    context = "\n\n".join(
        f"Source: {doc.metadata.get('source')}\nContent: {doc.page_content}"
        for doc in state["kb_docs"]
    )
    
    answer = llm.invoke(f'''
You are a technical instructor.

Answer using ONLY the private KB context.

Rules:
- Beginner-friendly explanation.
- Do not invent unsupported details.
- Mention that the answer is based on the private KB.
- Include source type: Private KB.

Question:
{question}

Private KB context:
{context}
''').content

    return {
        "answer": answer,
        "source": "private_kb",
    }
    
    
# Node 8 -> generate answer from web search

def generate_from_web(state: AgentState):
    question = state["question"]
    web_context = state["web_results"]

    answer = llm.invoke(f'''
You are a technical instructor.

The private KB was insufficient, so web search was used.

Answer using ONLY the web search context.

Rules:
- Beginner-friendly explanation.
- Do not invent unsupported details.
- Mention that the answer is based on Tavily web search.
- Include source type: Web Search.
- If URLs are present in context, include the most useful URLs.

Question:
{question}

Web search context:
{web_context}
''').content

    return {
        "answer": answer,
        "source": "web_search",
    }
    
# Node 9 -> Direct answer for general questions
def direct_ans(state: AgentState):
    question = state["question"]

    answer = llm.invoke(f'''
Respond briefly and naturally.

Message:
{question}
''').content

    return {
        "answer": answer,
        "source": "direct",
    }
    
    
# Node 10 -> Insufficient evidence answer
def insufficient_ans(state: AgentState):
    answer = (
        "I could not find enough reliable evidence in the private knowledge base "
        "or the web search results to answer this confidently. "
        "Please provide more specific documents or rephrase the question."
    )

    return {
        "answer": answer,
        "source": "insufficient_evidence",
    }