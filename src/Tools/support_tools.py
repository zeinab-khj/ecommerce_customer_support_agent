def log_payment_dispute(
    user_id: str,
    transaction_id: str,
    reason: str,
) -> dict:

    return {
        "success": True,
        "user_id": user_id,
        "transaction_id": transaction_id,
        "status": "payment_dispute_logged",
        "reason": reason,
    }


def log_complaint(
    user_id: str,
    complaint: str,
) -> dict:

    return {
        "success": True,
        "user_id": user_id,
        "status": "complaint_logged",
        "complaint": complaint,
    }


def escalate_to_agent(
    reason: str,
    priority: str,
    context_summary: str | None = None,
) -> dict:

    return {
        "success": True,
        "status": "escalated",
        "priority": priority,
        "reason": reason,
        "context_summary": context_summary,
    }
