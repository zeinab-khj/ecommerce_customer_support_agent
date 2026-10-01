from typing import Any


def run_agent(
    agent,
    evaluation_dataset: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    results = []

    for index, sample in enumerate(
        evaluation_dataset,
        start=1,
    ):
        try:
            output = agent.invoke(
                {
                    "user_request": sample["prompt"]
                }
            )

            result = {
                "id": sample["id"],
                "prompt": sample["prompt"],
                "true_route": sample.get("true_route"),
                "true_tool": sample.get("true_tool"),
                "true_arguments": sample.get(
                    "true_arguments"
                ),
                "reference_response": sample.get(
                    "reference_response"
                ),
                "predicted_route": output.get(
                    "route"
                ),
                "predicted_tool": output.get(
                    "selected_tool"
                ),
                "predicted_arguments": output.get(
                    "tool_arguments"
                ),
                "validation_status": output.get(
                    "validation_status"
                ),
                "validation_errors": output.get(
                    "validation_errors", []
                ),
                "guardrail_result": output.get(
                    "guardrail_result"
                ),
                "execution_status": output.get(
                    "execution_status"
                ),
                "tool_result": output.get(
                    "tool_result"
                ),
                "retrieved_documents": output.get(
                    "retrieved_documents", []
                ),
                "final_response": output.get(
                    "final_response"
                ),
                "escalation_required": output.get(
                    "escalation_required",
                    False,
                ),
                "escalation_reason": output.get(
                    "escalation_reason"
                ),
                "error": None,
            }

        except Exception as exc:
            result = {
                "id": sample["id"],
                "prompt": sample["prompt"],
                "true_route": sample.get("true_route"),
                "true_tool": sample.get("true_tool"),
                "true_arguments": sample.get(
                    "true_arguments"
                ),
                "reference_response": sample.get(
                    "reference_response"
                ),
                "predicted_route": None,
                "predicted_tool": None,
                "predicted_arguments": None,
                "validation_status": None,
                "validation_errors": [],
                "guardrail_result": None,
                "execution_status": None,
                "tool_result": None,
                "retrieved_documents": [],
                "final_response": None,
                "escalation_required": False,
                "escalation_reason": None,
                "error": str(exc),
            }

        results.append(result)

        print(
            f"[{index}/{len(evaluation_dataset)}] "
            f"{sample['id']}"
        )

    return results
