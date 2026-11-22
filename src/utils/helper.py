from src.state.state import AgentState
from src.workflows.workflows import agent_graph

def ask_agent(question: str):
    initial_state: AgentState = {
        "question": question,
        "current_query": question,
        "kb_docs": [],
        "web_results": "",
        "grade_kb": "",
        "grade_web": "",
        "answer": "",
        "source": "",
        "retry_count": 0,
    }
    
    return agent_graph.invoke(initial_state)