from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import (
    input_guard_node,
    router_node,
    retrieve_node,
    generate_response_node,
    clarification_node,
    human_escalation_node,
    tool_selection_node,
    tool_validation_node,
    guardrail_node,
    tool_execution_node,
    output_guard_node,
)


def route_after_router(
    state: AgentState,
) -> str:

    route = state.get("route")

    if route not in {
        "direct",
        "rag",
        "tool",
        "clarification",
        "human",
    }:
        raise ValueError(
            f"Invalid route: {route}"
        )

    return route


def route_after_validation(
    state: AgentState,
) -> str:

    validation_status = state.get(
        "validation_status"
    )

    if validation_status == "valid":
        return "valid"

    if validation_status == "invalid":
        return "invalid"

    raise ValueError(
        f"Invalid validation status: "
        f"{validation_status}"
    )


def route_after_guardrail(
    state: AgentState,
) -> str:

    result = state.get(
        "guardrail_result"
    )

    if result == "allowed":
        return "allowed"

    if result in {
        "requires_review",
        "blocked",
    }:
        return "human"

    raise ValueError(
        f"Invalid guardrail result: {result}"
    )


def build_graph(
    router,
    llm,
    retriever,
    tool_selector,
    available_tools,
    tool_registry,
):

    graph = StateGraph(AgentState)

    # -------------------------
    # Nodes
    # -------------------------

    graph.add_node(
        "input_guard",
        input_guard_node,
    )

    graph.add_node(
        "router",
        lambda state: router_node(
            state,
            router,
        ),
    )

    graph.add_node(
        "direct",
        lambda state: generate_response_node(
            state,
            llm,
        ),
    )

    graph.add_node(
        "retrieve",
        lambda state: retrieve_node(
            state,
            retriever,
        ),
    )

    graph.add_node(
        "generate_response",
        lambda state: generate_response_node(
            state,
            llm,
        ),
    )

    graph.add_node(
        "clarification",
        lambda state: clarification_node(
            state,
            llm,
        ),
    )

    graph.add_node(
        "human_escalation",
        lambda state: human_escalation_node(
            state,
            llm,
        ),
    )

    graph.add_node(
        "tool_selection",
        lambda state: tool_selection_node(
            state,
            tool_selector,
            available_tools,
        ),
    )

    graph.add_node(
        "tool_validation",
        lambda state: tool_validation_node(
            state,
            available_tools,
        ),
    )

    graph.add_node(
        "guardrail",
        guardrail_node,
    )

    graph.add_node(
        "tool_execution",
        lambda state: tool_execution_node(
            state,
            tool_registry,
        ),
    )

    graph.add_node(
        "output_guard",
        output_guard_node,
    )

    # -------------------------
    # Entry
    # -------------------------

    graph.add_edge(
        START,
        "input_guard",
    )

    graph.add_edge(
        "input_guard",
        "router",
    )

    # -------------------------
    # Router
    # -------------------------

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "direct": "direct",
            "rag": "retrieve",
            "tool": "tool_selection",
            "clarification": "clarification",
            "human": "human_escalation",
        },
    )

    # -------------------------
    # Direct
    # -------------------------

    graph.add_edge(
        "direct",
        "output_guard",
    )

    # -------------------------
    # RAG
    # -------------------------

    graph.add_edge(
        "retrieve",
        "generate_response",
    )

    graph.add_edge(
        "generate_response",
        "output_guard",
    )

    # -------------------------
    # Clarification
    # -------------------------

    graph.add_edge(
        "clarification",
        "output_guard",
    )

    # -------------------------
    # Human
    # -------------------------

    graph.add_edge(
        "human_escalation",
        "output_guard",
    )

    # -------------------------
    # Tool
    # -------------------------

    graph.add_edge(
        "tool_selection",
        "tool_validation",
    )

    graph.add_conditional_edges(
        "tool_validation",
        route_after_validation,
        {
            "valid": "guardrail",
            "invalid": "clarification",
        },
    )

    graph.add_conditional_edges(
        "guardrail",
        route_after_guardrail,
        {
            "allowed": "tool_execution",
            "human": "human_escalation",
        },
    )

    graph.add_edge(
        "tool_execution",
        "generate_response",
    )

    # -------------------------
    # Output
    # -------------------------

    graph.add_edge(
        "output_guard",
        END,
    )

    return graph.compile()
