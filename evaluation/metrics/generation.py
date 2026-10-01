from typing import Callable


def exact_match(
    prediction: str,
    reference: str,
) -> float:
    return float(
        prediction.strip() == reference.strip()
    )


def normalized_exact_match(
    prediction: str,
    reference: str,
) -> float:
    prediction = " ".join(
        prediction.lower().split()
    )

    reference = " ".join(
        reference.lower().split()
    )

    return float(prediction == reference)


def batch_exact_match(
    predictions: list[str],
    references: list[str],
) -> float:
    if len(predictions) != len(references):
        raise ValueError(
            "predictions and references "
            "must have the same length."
        )

    if not predictions:
        return 0.0

    return sum(
        normalized_exact_match(pred, ref)
        for pred, ref
        in zip(predictions, references)
    ) / len(predictions)


def judge_score(
    prediction: str,
    reference: str,
    judge: Callable[[str, str], float],
) -> float:
    return judge(prediction, reference)


def mean_judge_score(
    predictions: list[str],
    references: list[str],
    judge: Callable[[str, str], float],
) -> float:
    if len(predictions) != len(references):
        raise ValueError(
            "predictions and references "
            "must have the same length."
        )

    if not predictions:
        return 0.0

    scores = [
        judge(prediction, reference)
        for prediction, reference
        in zip(predictions, references)
    ]

    return sum(scores) / len(scores)
