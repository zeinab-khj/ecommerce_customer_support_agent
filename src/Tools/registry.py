from typing import Any, Callable


ToolFunction = Callable[..., Any]


TOOL_REGISTRY: dict[str, ToolFunction] = {}
