from typing import Any

from .graph import build_graph
from .llm import (
    build_llm,
    build_router,
    build_tool_selector,
)
from ..tools.registry import TOOL_REGISTRY


def build_agent(
    retriever: Any,
    available_tools: list[dict[str, Any]],
):
    router = build_router()
    llm = build_llm()
    tool_selector = build_tool_selector()

    agent = build_graph(
        router=router,
        llm=llm,
        retriever=retriever,
        tool_selector=tool_selector,
        available_tools=available_tools,
        tool_registry=TOOL_REGISTRY,
    )

    return agent
