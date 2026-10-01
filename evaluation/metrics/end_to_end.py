def task_success_rate(
    successful_tasks: list[bool],
) -> float:
    if not successful_tasks:
        return 0.0

    return sum(successful_tasks) / len(successful_tasks)


def recovery_success_rate(
    recoveries: list[bool],
) -> float:
    if not recoveries:
        return 0.0

    return sum(recoveries) / len(recoveries)


def failure_rate(
    failures: list[bool],
) -> float:
    if not failures:
        return 0.0

    return sum(failures) / len(failures)
