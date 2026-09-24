from typing import Any

from .graph import build_graph
from .llm import (
    build_llm,
    build_router,
    build_tool_selector,
)
from ..tools.registry import TOOL_REGISTRY
from ..tools.schemas import TOOL_SCHEMAS


def build_agent(
    retriever: Any,
):
    router = build_router()
    llm = build_llm()
    tool_selector = build_tool_selector()

    agent = build_graph(
        router=router,
        llm=llm,
        retriever=retriever,
        tool_selector=tool_selector,
        available_tools=TOOL_SCHEMAS,
        tool_registry=TOOL_REGISTRY,
    )

    return agent
