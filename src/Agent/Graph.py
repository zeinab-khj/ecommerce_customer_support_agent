from langgraph.graph import END, StateGraph

from .state import AgentState
from .nodes import input_guard_node, router_node
from .llm import build_router


def build_graph():
    router = build_router()

    graph = StateGraph(AgentState)

    graph.add_node(
        "input_guard",
        input_guard_node,
    )

    graph.add_node(
        "router",
        lambda state: router_node(state, router),
    )

    graph.set_entry_point("input_guard")

    graph.add_edge(
        "input_guard",
        "router",
    )

    graph.add_edge(
        "router",
        END,
    )

    return graph.compile()
