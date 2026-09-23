from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    messages: list[dict[str, Any]]
    user_request: str

    route: str
    route_reason: str
    missing_information: list[str]

    retrieved_documents: list[dict[str, Any]]

    selected_tool: str | None
    tool_arguments: dict[str, Any] | None
    tool_result: Any

    validation_status: str | None

    guardrail_result: str | None

    escalation_required: bool
    escalation_reason: str | None

    final_response: str | None
