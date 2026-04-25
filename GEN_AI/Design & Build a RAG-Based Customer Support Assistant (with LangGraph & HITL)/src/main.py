import argparse
from pathlib import Path

from src.config import AppConfig
from src.document_pipeline import build_vector_store, load_vector_store
from src.graph_workflow import build_graph


def cli_human_response_provider(state):
    print("\n[HITL ESCALATION TRIGGERED]")
    print(f"Intent: {state.get('intent')}")
    print(f"Confidence: {state.get('confidence')}")
    print("Top retrieved citations:")
    for cite in state.get("citations", []):
        print(f"- {cite}")
    print("\nEnter human agent response:")
    return input("> ").strip() or "A human support agent will contact you shortly."


def run_ingestion(pdf_path: str, config: AppConfig):
    build_vector_store(
        pdf_path=pdf_path,
        persist_dir=config.chroma_persist_dir,
        embedding_model=config.embedding_model,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    print("Ingestion completed successfully.")


def run_chat(config: AppConfig):
    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required in environment variables.")

    if not Path(config.chroma_persist_dir).exists():
        raise FileNotFoundError(
            "Vector store not found. Run ingestion first with --ingest path/to/file.pdf"
        )

    vector_store = load_vector_store(
        persist_dir=config.chroma_persist_dir,
        embedding_model=config.embedding_model,
    )

    app = build_graph(
        config=config,
        vector_store=vector_store,
        human_response_provider=cli_human_response_provider,
    )

    print("Customer Support Assistant is ready. Type 'exit' to quit.")
    while True:
        query = input("\nUser> ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        state = {"query": query}
        result = app.invoke(state)

        print("\nAssistant>", result.get("final_answer", "No answer produced."))
        print(f"Route: {result.get('route')} | Confidence: {result.get('confidence')}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="RAG-based customer support assistant (LangGraph + HITL)"
    )
    parser.add_argument(
        "--ingest",
        type=str,
        help="Path to PDF for knowledge base ingestion",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = AppConfig.from_env()

    if args.ingest:
        run_ingestion(args.ingest, config)
    else:
        run_chat(config)


if __name__ == "__main__":
    main()
