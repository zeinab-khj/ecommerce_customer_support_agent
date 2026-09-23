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

def router_node(
    state: AgentState,
    router,
) -> dict[str, Any]:

    user_request = state["user_request"]

    decision: RouteDecision = router.invoke(
        {
            "user_request": user_request
        }
    )

    return {
        "route": decision.route,
        "route_reason": decision.reason,
        "missing_information": decision.missing_information,
    }




def direct_node( state: AgentState, llm,) -> dict[str, Any]:

    user_request = state["user_request"]

    response = llm.invoke(
        user_request
    )

    return {
        "final_response": response.content,
    }


def retrieve_node(
    state: AgentState,
    retriever,
) -> dict[str, Any]:

    user_request = state["user_request"]

    documents = retriever.invoke(user_request)

    retrieved_documents = [
        {
            "content": document.page_content,
            "metadata": document.metadata,
        }
        for document in documents
    ]

    return {
        "retrieved_documents": retrieved_documents,
    }


def generate_response_node(
    state: AgentState,
    llm,
) -> dict[str, Any]:

    response = llm.invoke(
        {
            "user_request": state["user_request"],
            "retrieved_documents": state.get(
                "retrieved_documents",
                []
            ),
            "tool_result": state.get(
                "tool_result",
                None
            ),
        }
    )

    return {
        "final_response": response.content,
    }


def clarification_node(
    state: AgentState,
    llm,
) -> dict[str, Any]:

    user_request = state["user_request"]

    prompt = f"""
The user wants help with the following request:

{user_request}

The request cannot be completed yet because required information
is missing.

Ask the user for the minimum information needed to proceed.
Do not invent any information.
Be concise and natural.
"""

    response = llm.invoke(prompt)

    return {
        "final_response": response.content,
    }
