from math import log2


def recall_at_k(
    relevant_ids: set[str],
    retrieved_ids: list[str],
    k: int,
) -> float:
    if not relevant_ids:
        return 0.0

    retrieved = set(retrieved_ids[:k])

    return len(
        relevant_ids & retrieved
    ) / len(relevant_ids)


def precision_at_k(
    relevant_ids: set[str],
    retrieved_ids: list[str],
    k: int,
) -> float:
    if k <= 0:
        return 0.0

    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    relevant = sum(
        document_id in relevant_ids
        for document_id in retrieved
    )

    return relevant / len(retrieved)


def reciprocal_rank(
    relevant_ids: set[str],
    retrieved_ids: list[str],
) -> float:
    for rank, document_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if document_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    relevant_sets: list[set[str]],
    retrieved_lists: list[list[str]],
) -> float:
    if len(relevant_sets) != len(retrieved_lists):
        raise ValueError(
            "relevant_sets and retrieved_lists "
            "must have the same length."
        )

    if not relevant_sets:
        return 0.0

    scores = [
        reciprocal_rank(relevant, retrieved)
        for relevant, retrieved
        in zip(relevant_sets, retrieved_lists)
    ]

    return sum(scores) / len(scores)


def ndcg_at_k(
    relevance_scores: list[float],
    k: int,
) -> float:
    scores = relevance_scores[:k]

    dcg = sum(
        (2 ** score - 1) / log2(rank + 1)
        for rank, score in enumerate(scores, start=1)
    )

    ideal_scores = sorted(
        relevance_scores,
        reverse=True,
    )[:k]

    idcg = sum(
        (2 ** score - 1) / log2(rank + 1)
        for rank, score in enumerate(
            ideal_scores,
            start=1,
        )
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg
