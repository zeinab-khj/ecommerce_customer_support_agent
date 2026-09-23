from pydantic import BaseModel, Field
from typing import Any

from .routing import Route


class RouteDecision(BaseModel):
    route: Route = Field(
        description="The high-level route for the user request."
    )

    reason: str = Field(
        description="A concise explanation for the routing decision."
    )

    missing_information: list[str] = Field(
        default_factory=list,
        description=(
            "Information that is required to proceed but is missing "
            "from the user's request. Empty when nothing is missing."
        ),
    )


class ToolCallDecision(BaseModel):
    tool_name: str = Field(
        description="The name of the tool to call."
    )

    arguments: dict[str, Any] = Field(
        description="Arguments to pass to the selected tool."
    )

    reason: str = Field(
        description="A concise explanation for selecting this tool."
    )

class ToolValidationResult(BaseModel):
    valid: bool = Field(
        description="Whether the tool call is valid."
    )

    errors: list[str] = Field(
        default_factory=list,
        description="Validation errors, if any."
    )
