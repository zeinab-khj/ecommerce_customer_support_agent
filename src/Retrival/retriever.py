from langchain_core.documents import Document
from .vector_store import build_vector_store


def build_retriever(
    documents: list[Document],
    k: int = 5,
):
    vector_store = build_vector_store(
        documents
    )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
        },
    )
