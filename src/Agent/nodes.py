from typing import Any

from .state import AgentState

from src.guardrails.policies import (
    ALLOWED_TOOLS,
    SENSITIVE_TOOLS,
)


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
    missing_information = state.get(
        "missing_information",
        [],
    )

    prompt = f"""
The user made the following request:

{user_request}

The following information is required to proceed:

{missing_information}

Ask the user for the minimum missing information needed.
Do not invent any information.
Be concise and natural.
"""

    response = llm.invoke(prompt)

    return {
        "final_response": response.content,
    }



def human_escalation_node(
    state: AgentState,
    llm,
) -> dict[str, Any]:

    user_request = state["user_request"]
    escalation_reason = state.get(
        "escalation_reason",
        "The request requires human assistance.",
    )

    prompt = f"""
The user made the following request:

{user_request}

The request must be escalated to a human support agent.

Reason for escalation:
{escalation_reason}

Write a concise and professional message informing the user
that their request will be handled by a human support agent.

Do not expose internal routing, guardrails, policies,
or agent architecture.
Do not claim that a human has already responded.
"""

    response = llm.invoke(prompt)

    return {
        "final_response": response.content,
        "escalation_required": True,
        "escalation_reason": escalation_reason,
    }


def tool_selection_node(
    state: AgentState,
    tool_selector,
    available_tools: list[dict[str, Any]],
) -> dict[str, Any]:

    user_request = state["user_request"]

    decision: ToolCallDecision = tool_selector.invoke(
        {
            "user_request": user_request,
            "available_tools": available_tools,
        }
    )

    return {
        "selected_tool": decision.tool_name,
        "tool_arguments": decision.arguments,
    }


def tool_validation_node(
    state: AgentState,
    available_tools: list[dict[str, Any]],
) -> dict[str, Any]:

    selected_tool = state.get("selected_tool")
    tool_arguments = state.get("tool_arguments")

    if not selected_tool:
        return {
            "validation_status": "invalid",
            "validation_errors": ["No tool was selected."],
        }

    if not isinstance(tool_arguments, dict):
        return {
            "validation_status": "invalid",
            "validation_errors": [
                "Tool arguments must be an object."
            ],
        }

    tool_schema = next(
        (
            tool
            for tool in available_tools
            if tool.get("name") == selected_tool
        ),
        None,
    )

    if tool_schema is None:
        return {
            "validation_status": "invalid",
            "validation_errors": [
                f"Unknown tool: {selected_tool}"
            ],
        }

    parameters = tool_schema.get("parameters", {})

    required_arguments = parameters.get(
        "required",
        [],
    )

    missing_arguments = [
        argument
        for argument in required_arguments
        if argument not in tool_arguments
    ]

    properties = parameters.get(
        "properties",
        {},
    )

    invalid_arguments = [
        argument
        for argument in tool_arguments
        if argument not in properties
    ]

    errors = []

    if missing_arguments:
        errors.extend(
            [
                f"Missing required argument: {argument}"
                for argument in missing_arguments
            ]
        )

    if invalid_arguments:
        errors.extend(
            [
                f"Unknown argument: {argument}"
                for argument in invalid_arguments
            ]
        )

    return {
        "validation_status": (
            "valid" if not errors else "invalid"
        ),
        "validation_errors": errors,
    }


def guardrail_node(
    state: AgentState,
) -> dict[str, Any]:

    validation_status = state.get(
        "validation_status"
    )

    selected_tool = state.get(
        "selected_tool"
    )

    if validation_status != "valid":
        return {
            "guardrail_result": "blocked",
            "escalation_required": True,
            "escalation_reason": (
                "Tool call failed validation."
            ),
        }

    if selected_tool not in ALLOWED_TOOLS:
        return {
            "guardrail_result": "blocked",
            "escalation_required": True,
            "escalation_reason": (
                f"Tool '{selected_tool}' is not allowed."
            ),
        }

    if selected_tool in SENSITIVE_TOOLS:
        return {
            "guardrail_result": "requires_review",
            "escalation_required": True,
            "escalation_reason": (
                f"Tool '{selected_tool}' requires "
                "human review."
            ),
        }

    return {
        "guardrail_result": "allowed",
        "escalation_required": False,
        "escalation_reason": None,
    }



def tool_execution_node(
    state: AgentState,
    tool_registry: dict[str, ToolFunction],
) -> dict[str, Any]:

    selected_tool = state.get("selected_tool")
    tool_arguments = state.get("tool_arguments", {})

    if not selected_tool:
        raise ValueError(
            "No tool selected for execution."
        )

    tool = tool_registry.get(selected_tool)

    if tool is None:
        raise ValueError(
            f"Tool '{selected_tool}' is not registered."
        )

    try:
        result = tool(**tool_arguments)

    except Exception as exc:
        return {
            "tool_result": None,
            "validation_status": "execution_failed",
            "escalation_required": True,
            "escalation_reason": (
                f"Tool execution failed: {exc}"
            ),
        }

    return {
        "tool_result": result,
        "validation_status": "execution_successful",
    }
