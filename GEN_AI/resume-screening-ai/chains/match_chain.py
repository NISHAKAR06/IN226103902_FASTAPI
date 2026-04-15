from langchain_core.output_parsers import JsonOutputParser

from prompts.match_prompt import get_match_prompt


def build_match_chain(llm):
    prompt = get_match_prompt()
    parser = JsonOutputParser()
    return prompt | llm | parser
