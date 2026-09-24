from datasets import load_dataset

from agent.runtime import build_agent
from retrieval.documents import build_documents_from_dataset
from retrieval.retriever import build_retriever


DATASET_NAME = "rescommons/Full-Ecom-Chatbot-Dataset"


def build_runtime():
    dataset = load_dataset(
        DATASET_NAME,
    )

    train_dataset = dataset["train"]

    documents = build_documents_from_dataset(
        train_dataset,
    )

    if not documents:
        raise ValueError(
            "No knowledge documents were found."
        )

    retriever = build_retriever(
        documents,
        k=5,
    )

    agent = build_agent(
        retriever=retriever,
    )

    return agent
