from collections import Counter
from typing import Sequence


ROUTES = {
    "direct",
    "rag",
    "tool",
    "clarification",
    "human",
}


def routing_accuracy(
    y_true: Sequence[str],
    y_pred: Sequence[str],
) -> float:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    if not y_true:
        return 0.0

    correct = sum(
        true == pred
        for true, pred in zip(y_true, y_pred)
    )

    return correct / len(y_true)


def routing_confusion_matrix(
    y_true: Sequence[str],
    y_pred: Sequence[str],
) -> dict[str, dict[str, int]]:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    matrix = {
        true_route: {
            predicted_route: 0
            for predicted_route in ROUTES
        }
        for true_route in ROUTES
    }

    for true, pred in zip(y_true, y_pred):
        if true not in ROUTES:
            raise ValueError(f"Unknown true route: {true}")

        if pred not in ROUTES:
            raise ValueError(f"Unknown predicted route: {pred}")

        matrix[true][pred] += 1

    return matrix


def routing_per_class_metrics(
    y_true: Sequence[str],
    y_pred: Sequence[str],
) -> dict[str, dict[str, float]]:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    metrics = {}

    for route in ROUTES:
        tp = sum(
            true == route and pred == route
            for true, pred in zip(y_true, y_pred)
        )

        fp = sum(
            true != route and pred == route
            for true, pred in zip(y_true, y_pred)
        )

        fn = sum(
            true == route and pred != route
            for true, pred in zip(y_true, y_pred)
        )

        precision = (
            tp / (tp + fp)
            if tp + fp > 0
            else 0.0
        )

        recall = (
            tp / (tp + fn)
            if tp + fn > 0
            else 0.0
        )

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0
            else 0.0
        )

        metrics[route] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    return metrics


def macro_f1(
    y_true: Sequence[str],
    y_pred: Sequence[str],
) -> float:
    per_class = routing_per_class_metrics(y_true, y_pred)

    if not per_class:
        return 0.0

    return sum(
        values["f1"]
        for values in per_class.values()
    ) / len(per_class)
