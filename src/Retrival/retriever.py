from langchain_core.vectorstores import VectorStoreRetriever

from .vector_store import build_vector_store


def build_retriever(documents) -> VectorStoreRetriever:
    vector_store = build_vector_store(documents)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5,
        },
    )

    return retriever
