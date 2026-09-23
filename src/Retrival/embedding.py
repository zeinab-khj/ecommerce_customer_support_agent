from langchain_huggingface import HuggingFaceEmbeddings


def build_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


