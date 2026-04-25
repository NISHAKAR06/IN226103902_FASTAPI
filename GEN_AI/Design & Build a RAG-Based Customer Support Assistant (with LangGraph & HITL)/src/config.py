import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class AppConfig:
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_persist_dir: str = "./chroma_db"
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 4
    confidence_threshold: float = 0.65


    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            embedding_model=os.getenv(
                "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
            ),
            chroma_persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
            chunk_size=int(os.getenv("CHUNK_SIZE", "800")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "120")),
            top_k=int(os.getenv("TOP_K", "4")),
            confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", "0.65")),
        )
