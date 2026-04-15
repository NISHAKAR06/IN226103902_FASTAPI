from prompts.explain_prompt import get_explain_prompt


def build_explain_chain(llm):
    prompt = get_explain_prompt()
    return prompt | llm
