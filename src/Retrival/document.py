import json
from typing import Any

from langchain_core.documents import Document


def build_documents_from_dataset(
    dataset,
) -> list[Document]:

    documents = []
    seen_contents = set()

    for row in dataset:
        context = row.get("context")

        if not context:
            continue

        if isinstance(context, str):
            try:
                context = json.loads(context)
            except json.JSONDecodeError:
                continue

        if not isinstance(context, dict):
            continue

        retrieved_docs = context.get(
            "retrieved_docs",
            [],
        )

        if not isinstance(retrieved_docs, list):
            continue

        for item in retrieved_docs:

            if isinstance(item, str):
                content = item
                metadata = {}

            elif isinstance(item, dict):
                content = (
                    item.get("content")
                    or item.get("text")
                    or item.get("page_content")
                )

                metadata = {
                    key: value
                    for key, value in item.items()
                    if key not in {
                        "content",
                        "text",
                        "page_content",
                    }
                }

            else:
                continue

            if not isinstance(content, str):
                continue

            content = content.strip()

            if not content:
                continue

            if content in seen_contents:
                continue

            seen_contents.add(content)

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata,
                )
            )

    return documents
