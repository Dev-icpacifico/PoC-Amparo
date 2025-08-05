from langgraph.graph import START, StateGraph

from app.graph.nodes import amparo_node, supervisor_node, retriever_node
from app.graph.schema import GlobalState
from app.persistence.checkpointer_sqlite import checkpointer

builder = StateGraph(GlobalState)
# builder.add_edge(START, "supervisor")
builder.add_edge(START, "amparo")
builder.add_node("amparo", amparo_node)
builder.add_node("supervisor", supervisor_node)
builder.add_node("consultas",retriever_node)

graph =  builder.compile(checkpointer=checkpointer)



with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
