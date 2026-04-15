from langchain_core.prompts import PromptTemplate


def get_extract_prompt():
    return PromptTemplate.from_template(
        """You are a resume parsing assistant.
Extract only information that is explicitly present in the resume text.
Do not infer or invent skills, tools, employers, or experience.

Return a valid JSON object with this schema:
{{
  "name": string | null,
  "email": string | null,
  "phone": string | null,
  "skills": [string],
  "tools": [string],
  "experience": [string],
  "education": [string],
  "projects": [string],
  "summary": string
}}

Resume text:
{resume_text}
"""
    )
