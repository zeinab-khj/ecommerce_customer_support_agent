from typing import Any

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from .embeddings import build_embedding_model


def build_vector_store(
    documents: list[Document],
) -> FAISS:
    embedding_model = build_embedding_model()

    vector_store = FAISS.from_documents(
        documents,
        embedding_model,
    )

    return vector_store
