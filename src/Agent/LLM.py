import os

from langchain_openai import ChatOpenAI

from .schemas import RouteDecision


def build_router():
    """
    Build the LLM-based router.

    The router is configured to return a structured
    RouteDecision instead of free-form text.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set."
        )

    llm = ChatOpenAI(
        model="gpt-5.6-luna",
        temperature=0,
    )

    router = llm.with_structured_output(RouteDecision)

    return router
