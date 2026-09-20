from typing import Literal

from .state import AgentState


Route = Literal[
    "direct",
    "rag",
    "tool",
    "clarification",
    "human",
]


def route_request(state: AgentState) -> Route:
    """
    Determine the next high-level route for the agent.

    The actual routing decision will later be produced by
    an LLM-based router. This function provides a typed
    interface for that decision.
    """

    route = state.get("route")

    if route not in {
        "direct",
        "rag",
        "tool",
        "clarification",
        "human",
    }:
        raise ValueError(f"Invalid route: {route}")

    return route
