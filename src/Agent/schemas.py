from pydantic import BaseModel, Field

from .routing import Route


class RouteDecision(BaseModel):
    route: Route = Field(
        description="The high-level route for the user request."
    )
    reason: str = Field(
        description="A concise explanation for the routing decision."
    )
