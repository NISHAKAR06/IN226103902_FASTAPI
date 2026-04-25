# RAG Internship Project
## Design & Build a RAG-Based Customer Support Assistant (LangGraph + HITL)

This folder contains complete internship deliverables:
- High-Level Design (HLD)
- Low-Level Design (LLD)
- Technical Documentation
- Working implementation (PDF -> ChromaDB -> Retrieval -> LangGraph routing -> HITL)

## Folder Structure
```text
.
├── docs/
│   ├── HLD.md
│   ├── LLD.md
│   └── Technical_Documentation.md
├── diagrams/
│   ├── architecture.mmd
│   └── langgraph_flow.mmd
├── prompts/
│   └── system_prompt.txt
├── src/
│   ├── main.py
│   ├── config.py
│   ├── document_pipeline.py
│   ├── retriever.py
│   ├── routing.py
│   ├── hitl.py
│   ├── graph_workflow.py
│   └── schemas.py
├── chroma_db/
├── data/
├── .env.example
└── requirements.txt
```

## Mandatory Concepts Covered
- RAG pipeline: PDF load -> chunk -> embeddings -> ChromaDB -> retrieval -> answer
- LangGraph workflow: Input -> Processing Node -> Output Node
- Conditional intent/confidence routing
- Human-in-the-Loop escalation

## Setup
1. Open terminal in this folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and set `OPENAI_API_KEY`.

## Usage
### 1) Ingest PDF knowledge base
```bash
python -m src.main --ingest "data/knowledge_base.pdf"
```

### 2) Start assistant chat
```bash
python -m src.main
```

If a query is complex, sensitive, or low-confidence, HITL will be triggered and you can provide a human response directly in the CLI.

## PDF Deliverables
The required source documents are in `docs/`:
- `docs/HLD.md`
- `docs/LLD.md`
- `docs/Technical_Documentation.md`

You can convert these files to PDF with a Markdown-to-PDF tool such as Pandoc:

```bash
pandoc docs/HLD.md -o docs/HLD.pdf
pandoc docs/LLD.md -o docs/LLD.pdf
pandoc docs/Technical_Documentation.md -o docs/Technical_Documentation.pdf
```

## Suggested Sample Questions
- How do I reset my password?
- I was charged twice, can I get a refund?
- What is your enterprise support SLA?

## Notes
- This is designed as a production-style internship submission with clear architecture and implementation reasoning.
- The routing layer is intentionally transparent and easy to tune.
