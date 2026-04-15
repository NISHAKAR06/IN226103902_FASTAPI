from langchain_core.prompts import PromptTemplate


def get_explain_prompt():
    return PromptTemplate.from_template(
        """You are a resume screening explanation assistant.
Explain the score in clear, concise language for a recruiter.
Do not add facts that are not present in the inputs.

Return a plain-English explanation with:
- why the candidate fits or does not fit
- what strengths were observed
- what gaps limit the score
- one concise hiring note

Extracted resume:
{extracted_resume}

Match analysis:
{match_analysis}

Score analysis:
{score_analysis}
"""
    )
