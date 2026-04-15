# Resume Screening AI

This project implements a modular AI resume screening pipeline with LangChain and LangSmith tracing.

## Structure
- `prompts/`: reusable prompt templates
- `chains/`: LCEL chain builders
- `data/`: sample resumes and job description text files
- `main.py`: runs strong, average, and weak candidate evaluations

## Pipeline
Resume -> Skill extraction -> Matching -> Scoring -> Explanation

## Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables:

```bash
set OPENAI_API_KEY=your_key
set LANGCHAIN_TRACING_V2=true
set LANGCHAIN_API_KEY=your_langsmith_key
set LANGCHAIN_PROJECT=resume-screening-ai
```

Or create a `.env` file in this folder:

```env
OPENAI_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=resume-screening-ai
```

3. Run the project:

```bash
python main.py
```

To include a deliberately weak debug run for LangSmith troubleshooting:

```bash
python main.py --debug
```

## Notes
- The prompts explicitly forbid inventing missing skills or experience.
- Each stage is traced separately with tags for easier debugging in LangSmith.
- The sample data includes strong, average, and weak resumes for the required three runs.
- The optional `--debug` run is useful for capturing an obviously poor-fit case in tracing.
