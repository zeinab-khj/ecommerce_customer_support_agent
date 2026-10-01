def violation_rate(
    violations: list[bool],
) -> float:
    if not violations:
        return 0.0

    return sum(violations) / len(violations)


def safe_action_rate(
    unsafe_actions: list[bool],
) -> float:
    if not unsafe_actions:
        return 1.0

    return 1.0 - (
        sum(unsafe_actions) / len(unsafe_actions)
    )


def policy_compliance_rate(
    compliant: list[bool],
) -> float:
    if not compliant:
        return 0.0

    return sum(compliant) / len(compliant)
