from ..metrics.routing import (
    routing_accuracy,
    routing_macro_f1,
    routing_per_class_metrics,
    routing_confusion_matrix,
)

from ..metrics.tools import (
    tool_selection_accuracy,
    argument_key_precision,
    argument_key_recall,
    valid_tool_call_rate,
)

from ..metrics.generation import (
    mean_exact_match,
)


def evaluate_results(
    results: list[dict],
) -> dict:
    report = {}

    # -------------------------
    # Routing
    # -------------------------

    routing_results = [
        row
        for row in results
        if row.get("predicted_route") is not None
        and row.get("true_route") is not None
    ]

    true_routes = [
        row["true_route"]
        for row in routing_results
    ]

    predicted_routes = [
        row["predicted_route"]
        for row in routing_results
    ]

    report["routing"] = {
        "accuracy": routing_accuracy(
            true_routes,
            predicted_routes,
        ),
        "macro_f1": routing_macro_f1(
            true_routes,
            predicted_routes,
        ),
        "per_class": routing_per_class_metrics(
            true_routes,
            predicted_routes,
        ),
        "confusion_matrix": routing_confusion_matrix(
            true_routes,
            predicted_routes,
        ),
    }

    # -------------------------
    # Tool Calling
    # -------------------------

    tool_results = [
        row
        for row in results
        if row.get("true_tool") is not None
    ]

    true_tools = [
        row["true_tool"]
        for row in tool_results
    ]

    predicted_tools = [
        row["predicted_tool"]
        for row in tool_results
    ]

    report["tools"] = {
        "selection_accuracy": tool_selection_accuracy(
            true_tools,
            predicted_tools,
        ),
    }

    argument_precisions = []
    argument_recalls = []
    argument_exact_matches = []

    for row in tool_results:
        true_args = row.get("true_arguments") or {}
        predicted_args = row.get(
            "predicted_arguments"
        ) or {}

        argument_precisions.append(
            argument_key_precision(
                true_args,
                predicted_args,
            )
        )

        argument_recalls.append(
            argument_key_recall(
                true_args,
                predicted_args,
            )
        )

        argument_exact_matches.append(
            true_args == predicted_args
        )

    if tool_results:
        report["tools"]["argument_key_precision"] = (
            sum(argument_precisions)
            / len(argument_precisions)
        )

        report["tools"]["argument_key_recall"] = (
            sum(argument_recalls)
            / len(argument_recalls)
        )

        report["tools"]["argument_exact_match"] = (
            sum(argument_exact_matches)
            / len(argument_exact_matches)
        )

    validation_statuses = [
        row["validation_status"]
        for row in results
        if row.get("validation_status") is not None
    ]

    report["tools"]["valid_call_rate"] = (
        valid_tool_call_rate(
            validation_statuses
        )
    )

    # -------------------------
    # Generation
    # -------------------------

    generation_results = [
        row
        for row in results
        if row.get("final_response")
        and row.get("reference_response")
        and isinstance(
            row["reference_response"],
            str,
        )
    ]

    predictions = [
        row["final_response"]
        for row in generation_results
    ]

    references = [
        row["reference_response"]
        for row in generation_results
    ]

    report["generation"] = {
        "normalized_exact_match": mean_exact_match(
            predictions,
            references,
        )
    }

    # -------------------------
    # End-to-End
    # -------------------------

    successful_tasks = []

    for row in results:
        route_correct = (
            row.get("true_route")
            == row.get("predicted_route")
        )

        tool_correct = True

        if row.get("true_tool") is not None:
            tool_correct = (
                row.get("true_tool")
                == row.get("predicted_tool")
            )

        no_error = row.get("error") is None

        successful_tasks.append(
            route_correct
            and tool_correct
            and no_error
        )

    report["end_to_end"] = {
        "task_success_rate": (
            sum(successful_tasks)
            / len(successful_tasks)
            if successful_tasks
            else 0.0
        ),
        "error_rate": (
            sum(
                row.get("error") is not None
                for row in results
            )
            / len(results)
            if results
            else 0.0
        ),
    }

    return report
