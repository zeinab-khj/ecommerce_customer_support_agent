from typing import Any


def tool_selection_accuracy(
    true_tools: list[str | None],
    predicted_tools: list[str | None],
) -> float:
    if len(true_tools) != len(predicted_tools):
        raise ValueError(
            "true_tools and predicted_tools must have the same length."
        )

    if not true_tools:
        return 0.0

    correct = sum(
        true_tool == predicted_tool
        for true_tool, predicted_tool
        in zip(true_tools, predicted_tools)
    )

    return correct / len(true_tools)


def argument_exact_match(
    true_arguments: dict[str, Any],
    predicted_arguments: dict[str, Any],
) -> bool:
    return true_arguments == predicted_arguments


def argument_key_recall(
    true_arguments: dict[str, Any],
    predicted_arguments: dict[str, Any],
) -> float:
    required_keys = set(true_arguments)

    if not required_keys:
        return 1.0

    predicted_keys = set(predicted_arguments)

    return len(
        required_keys & predicted_keys
    ) / len(required_keys)


def argument_key_precision(
    true_arguments: dict[str, Any],
    predicted_arguments: dict[str, Any],
) -> float:
    predicted_keys = set(predicted_arguments)

    if not predicted_keys:
        return 1.0 if not true_arguments else 0.0

    true_keys = set(true_arguments)

    return len(
        true_keys & predicted_keys
    ) / len(predicted_keys)


def valid_tool_call_rate(
    validation_statuses: list[str],
) -> float:
    if not validation_statuses:
        return 0.0

    valid = sum(
        status == "valid"
        for status in validation_statuses
    )

    return valid / len(validation_statuses)


def invalid_tool_call_rate(
    validation_statuses: list[str],
) -> float:
    return 1.0 - valid_tool_call_rate(
        validation_statuses
    )
