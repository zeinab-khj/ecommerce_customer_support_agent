from pydantic import BaseModel, Field

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
