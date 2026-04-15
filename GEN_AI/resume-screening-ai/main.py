import json
import os
import sys
from pathlib import Path

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from chains.explain_chain import build_explain_chain
from chains.extract_chain import build_extract_chain
from chains.match_chain import build_match_chain
from chains.score_chain import build_score_chain


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

load_dotenv()


def load_text(file_name: str) -> str:
    return (DATA_DIR / file_name).read_text(encoding="utf-8")


def build_llm() -> ChatOpenAI:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Set it in your environment or create a .env file in this folder."
        )
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model_name, temperature=0)


def run_pipeline(resume_text: str, job_description: str, label: str):
    llm = build_llm()
    extract_chain = build_extract_chain(llm)
    match_chain = build_match_chain(llm)
    score_chain = build_score_chain(llm)
    explain_chain = build_explain_chain(llm)

    extracted_resume = extract_chain.invoke(
        {"resume_text": resume_text},
        config={"tags": ["resume-screening", label, "extract"]},
    )
    match_analysis = match_chain.invoke(
        {
            "extracted_resume": json.dumps(extracted_resume, indent=2),
            "job_description": job_description,
        },
        config={"tags": ["resume-screening", label, "match"]},
    )
    score_analysis = score_chain.invoke(
        {
            "extracted_resume": json.dumps(extracted_resume, indent=2),
            "match_analysis": json.dumps(match_analysis, indent=2),
            "job_description": job_description,
        },
        config={"tags": ["resume-screening", label, "score"]},
    )
    explanation = explain_chain.invoke(
        {
            "extracted_resume": json.dumps(extracted_resume, indent=2),
            "match_analysis": json.dumps(match_analysis, indent=2),
            "score_analysis": json.dumps(score_analysis, indent=2),
        },
        config={"tags": ["resume-screening", label, "explain"]},
    )

    return {
        "label": label,
        "extracted_resume": extracted_resume,
        "match_analysis": match_analysis,
        "score_analysis": score_analysis,
        "explanation": explanation,
    }


def print_result(result: dict):
    print(f"\n=== {result['label'].upper()} CANDIDATE ===")
    print(f"Score: {result['score_analysis'].get('score')} / 100")
    print(f"Rating: {result['score_analysis'].get('rating')}")
    print("Explanation:")
    print(result["explanation"])


def main():
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    if tracing_enabled:
        print("LangSmith tracing is enabled.")
    else:
        print("LangSmith tracing is not enabled. Set LANGCHAIN_TRACING_V2=true to trace runs.")

    job_description = load_text("job_description.txt")
    samples = [
        ("strong_resume.txt", "strong"),
        ("avg_resume.txt", "average"),
        ("weak_resume.txt", "weak"),
    ]

    for file_name, label in samples:
        try:
            result = run_pipeline(load_text(file_name), job_description, label)
            print_result(result)
        except RuntimeError as exc:
            print(f"Setup error: {exc}")
            return

    if "--debug" in sys.argv:
        debug_resume = (
            "Name: Debug Candidate\n"
            "Summary: Interested in creative writing and customer support.\n"
            "Skills: Communication, MS Word\n"
            "Experience: Internship in content editing.\n"
        )
        print("\nRunning debug case for tracing diagnostics...")
        result = run_pipeline(debug_resume, job_description, "debug")
        print_result(result)


if __name__ == "__main__":
    main()
