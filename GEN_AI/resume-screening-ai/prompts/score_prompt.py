from langchain_core.prompts import PromptTemplate


def get_score_prompt():
        return PromptTemplate.from_template(
                """You are a resume scoring assistant.
Score the candidate from 0 to 100 based only on the provided extraction and matching results.
Use these guidelines:
- Strong alignment with most required skills: higher score
- Partial alignment with some gaps: medium score
- Limited alignment or weak experience: lower score

Return a valid JSON object with this schema:
{{
    "score": integer,
    "rating": string,
    "score_breakdown": {{
        "skills": integer,
        "experience": integer,
        "tools": integer,
        "education": integer
    }},
    "rationale": string
}}

Extracted resume:
{extracted_resume}

Match analysis:
{match_analysis}

Job description:
{job_description}
"""
        )
