from langchain_core.output_parsers import JsonOutputParser

from prompts.extract_prompt import get_extract_prompt


def build_extract_chain(llm):
    prompt = get_extract_prompt()
    parser = JsonOutputParser()
    return prompt | llm | parser
