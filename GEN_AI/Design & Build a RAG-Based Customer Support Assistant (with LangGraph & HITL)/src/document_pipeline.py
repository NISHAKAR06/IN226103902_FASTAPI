from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def get_embeddings_model(model_name: str) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=model_name)


def load_pdf_documents(pdf_path: str):
    path = Path(pdf_path)
    if not path.exists() or path.suffix.lower() != ".pdf":
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    return PyPDFLoader(str(path)).load()


def chunk_documents(docs, chunk_size: int, chunk_overlap: int):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_documents(docs)


def build_vector_store(
    pdf_path: str,
    persist_dir: str,
    embedding_model: str,
    chunk_size: int,
    chunk_overlap: int,
):
    docs = load_pdf_documents(pdf_path)
    chunks = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings_model(embedding_model),
        persist_directory=persist_dir,
    )
    vector_store.persist()
    return vector_store


def load_vector_store(persist_dir: str, embedding_model: str):
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=get_embeddings_model(embedding_model),
    )
