from typing import Any

from .state import AgentState


def input_guard_node(state: AgentState) -> dict[str, Any]:
    """
    Validate the incoming user request before routing.

    This node performs lightweight deterministic checks.
    """

    user_request = state.get("user_request")

    if not isinstance(user_request, str):
        raise ValueError("user_request must be a string.")

    user_request = user_request.strip()

    if not user_request:
        raise ValueError("user_request cannot be empty.")

    return {
        "user_request": user_request,
    }

def router_node(state: AgentState, router,) -> dict[str, Any]:
    """
    Determine the high-level route for the user request.
    """

    user_request = state["user_request"]

    decision: RouteDecision = router.invoke(
        user_request
    )

    return {
        "route": decision.route,
        "route_reason": decision.reason,
    }




def direct_node( state: AgentState, llm,) -> dict[str, Any]:

    user_request = state["user_request"]

    response = llm.invoke(
        user_request
    )

    return {
        "final_response": response.content,
    }
