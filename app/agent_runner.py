from langchain_core.messages import HumanMessage
from app.graph.builder import graph

def run_agent(user_id: str, mensaje: str, session_id: str = None):
    thread_id = session_id or user_id
    config = {"configurable": {"thread_id": thread_id, "user_id": user_id}}
    state = {
        "messages": [HumanMessage(content=mensaje)],
        "graph": "default",
        "next": "",
        "task_completed": False
    }
    result = graph.invoke(state, config=config)
    return result["messages"][-1].content
