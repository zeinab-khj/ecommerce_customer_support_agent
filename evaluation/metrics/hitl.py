def hitl_trigger_accuracy(
    should_escalate: list[bool],
    did_escalate: list[bool],
) -> float:
    if len(should_escalate) != len(did_escalate):
        raise ValueError(
            "should_escalate and did_escalate "
            "must have the same length."
        )

    if not should_escalate:
        return 0.0

    return sum(
        expected == actual
        for expected, actual
        in zip(should_escalate, did_escalate)
    ) / len(should_escalate)


def unnecessary_escalation_rate(
    should_escalate: list[bool],
    did_escalate: list[bool],
) -> float:
    if len(should_escalate) != len(did_escalate):
        raise ValueError(
            "Input lists must have the same length."
        )

    if not should_escalate:
        return 0.0

    unnecessary = sum(
        not expected and actual
        for expected, actual
        in zip(should_escalate, did_escalate)
    )

    return unnecessary / len(should_escalate)


def missed_escalation_rate(
    should_escalate: list[bool],
    did_escalate: list[bool],
) -> float:
    if len(should_escalate) != len(did_escalate):
        raise ValueError(
            "Input lists must have the same length."
        )

    if not should_escalate:
        return 0.0

    missed = sum(
        expected and not actual
        for expected, actual
        in zip(should_escalate, did_escalate)
    )

    return missed / len(should_escalate)
