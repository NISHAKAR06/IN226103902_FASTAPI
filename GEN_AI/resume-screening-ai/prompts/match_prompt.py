from langchain_core.prompts import PromptTemplate


def get_match_prompt():
    return PromptTemplate.from_template(
        """You are a resume matching assistant.
Compare the extracted resume information against the job description.
Use only the provided data. Do not assume skills or experience that are not present.

Return a valid JSON object with this schema:
{{
  "matched_skills": [string],
  "missing_skills": [string],
  "matched_tools": [string],
  "fit_summary": string,
  "match_strength": string
}}

Extracted resume:
{extracted_resume}

Job description:
{job_description}
"""
    )
