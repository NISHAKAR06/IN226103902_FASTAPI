from langchain_core.output_parsers import JsonOutputParser

from prompts.score_prompt import get_score_prompt


def build_score_chain(llm):
    prompt = get_score_prompt()
    parser = JsonOutputParser()
    return prompt | llm | parser
