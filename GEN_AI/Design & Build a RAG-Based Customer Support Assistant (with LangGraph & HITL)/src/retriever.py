from langchain_community.vectorstores import Chroma


def retrieve_context(query: str, vector_store: Chroma, k: int = 4):
    return vector_store.similarity_search(query, k=k)


def docs_to_context_and_citations(docs):
    contexts = [doc.page_content for doc in docs]
    citations = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "?")
        citations.append(f"{source}#page={page}")
    return contexts, citations
