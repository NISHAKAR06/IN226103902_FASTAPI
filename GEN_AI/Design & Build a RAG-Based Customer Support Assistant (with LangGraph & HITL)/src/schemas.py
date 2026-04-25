from typing import TypedDict


class GraphState(TypedDict, total=False):
    query: str
    intent: str
    contexts: list[str]
    citations: list[str]
    draft_answer: str
    final_answer: str
    confidence: float
    route: str
    escalated: bool
    human_response: str
    errors: list[str]
