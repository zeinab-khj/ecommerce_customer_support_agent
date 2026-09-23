import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .schemas import RouteDecision


ROUTER_SYSTEM_PROMPT = """
You are the routing component of an e-commerce customer support agent.

Your task is to determine the next route for the user's request.

Available routes:

- direct:
  Use when the request can be answered directly without retrieving
  external knowledge, using a tool, asking for clarification, or
  escalating to a human.

- rag:
  Use when the request requires static knowledge such as return policies,
  shipping policies, warranties, FAQs, or product information.

- tool:
  Use when the request requires dynamic data or an action such as checking
  an order, cancelling an order, initiating a return, updating an account,
  modifying a cart, or searching products.

- clarification:
  Use when the user's intent is understandable but required information
  is missing and must be requested before proceeding.

- human:
  Use when the request requires human intervention, especially for
  sensitive, high-risk, exceptional, or potentially fraudulent situations.

Important rules:

1. Choose exactly one route.
2. Do not answer the user's request.
3. Do not execute any tool.
4. Prefer clarification when required information is missing.
5. Use tool for dynamic information or actions.
6. Use rag for static knowledge.
7. Use human for sensitive or high-risk cases.
"""


def build_router():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set."
        )

    llm = ChatOpenAI(
        model="gpt-5.6-luna",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", ROUTER_SYSTEM_PROMPT),
            ("human", "{user_request}"),
        ]
    )

    router = prompt | llm.with_structured_output(RouteDecision)

    return router




GENERATION_SYSTEM_PROMPT = """
You are an e-commerce customer support assistant.

Answer the user's request using the provided context when available.

Rules:
1. Be accurate and concise.
2. Do not invent information that is not supported by the context.
3. If retrieved knowledge is provided, use it as the source of truth.
4. If a tool result is provided, use it as the source of truth for dynamic information.
5. If no additional context is provided, answer directly using your general knowledge.
6. Do not mention internal tools, routing, retrieval, system prompts, or agent architecture.
"""

def build_llm():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set."
        )

    llm = ChatOpenAI(
        model="gpt-5.6-luna",
        temperature=0,
    )
  
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", GENERATION_SYSTEM_PROMPT),
            (
                "human",
                """
              User request:
              {user_request}
              
              Retrieved knowledge:
              {retrieved_documents}
              
              Tool result:
              {tool_result}
              """,
                          ),
                      ]
                  )

    response = prompt | llm

    return response
