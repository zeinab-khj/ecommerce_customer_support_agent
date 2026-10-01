import json
import re
from typing import Any


ROUTES = {
    "direct",
    "rag",
    "tool",
    "clarification",
    "human",
}


def parse_json(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, (dict, list)):
        return value

    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None

    return None


def extract_tool_call(response: Any) -> dict[str, Any] | None:
    parsed = parse_json(response)

    if not isinstance(parsed, dict):
        return None

    if "name" not in parsed:
        return None

    if "arguments" not in parsed:
        return None

    if not isinstance(parsed["name"], str):
        return None

    if not isinstance(parsed["arguments"], dict):
        return None

    return {
        "name": parsed["name"],
        "arguments": parsed["arguments"],
    }


def has_retrieved_documents(context: Any) -> bool:
    parsed = parse_json(context)

    if not isinstance(parsed, dict):
        return False

    documents = parsed.get("retrieved_docs", [])

    return isinstance(documents, list) and len(documents) > 0


def looks_like_human_escalation(response: Any) -> bool:
    if not isinstance(response, str):
        return False

    text = response.lower()

    patterns = [
        "human agent",
        "support agent",
        "customer support agent",
        "escalate",
        "escalated",
        "human representative",
        "contact our support team",
    ]

    return any(
        pattern in text
        for pattern in patterns
    )


def looks_like_clarification(response: Any) -> bool:
    if not isinstance(response, str):
        return False

    text = response.strip().lower()

    clarification_patterns = [
        "could you provide",
        "please provide",
        "please specify",
        "can you provide",
        "what is your",
        "what's your",
        "which order",
        "which item",
        "could you tell me",
        "please confirm",
    ]

    return any(
        pattern in text
        for pattern in clarification_patterns
    )


def infer_route(row: dict[str, Any]) -> tuple[str, str]:
    response = row.get("response")
    context = row.get("context")

    # 1. Explicit tool call
    tool_call = extract_tool_call(response)

    if tool_call is not None:
        return "tool", "deterministic_tool_call"

    # 2. Human escalation
    if looks_like_human_escalation(response):
        return "human", "response_pattern"

    # 3. RAG / knowledge retrieval
    if has_retrieved_documents(context):
        return "rag", "retrieved_docs_present"

    # 4. Clarification
    if looks_like_clarification(response):
        return "clarification", "response_pattern"

    # 5. Default
    return "direct", "default"


def build_ground_truth_row(row: dict[str, Any]) -> dict[str, Any]:
    route, label_source = infer_route(row)

    tool_call = extract_tool_call(
        row.get("response")
    )

    return {
        "id": row.get("id"),
        "prompt": row.get("prompt"),
        "true_route": route,
        "route_label_source": label_source,
        "true_tool": (
            tool_call["name"]
            if tool_call
            else None
        ),
        "true_arguments": (
            tool_call["arguments"]
            if tool_call
            else None
        ),
        "reference_response": row.get("response"),
        "context": row.get("context"),
        "domain": row.get("domain"),
        "intent_category": row.get("intent_category"),
        "intent": row.get("intent"),
        "sub_intent": row.get("sub_intent"),
        "difficulty": row.get("difficulty"),
    }


def build_ground_truth(dataset) -> list[dict[str, Any]]:
    records = []

    for row in dataset:
        records.append(
            build_ground_truth_row(row)
        )

    return records
