from src.schemas import GraphState


def escalate_case(state: GraphState, human_response_provider) -> GraphState:
    state["escalated"] = True
    if callable(human_response_provider):
        human_text = human_response_provider(state)
    else:
        human_text = "A human support agent will follow up shortly."

    state["human_response"] = human_text
    state["final_answer"] = human_text
    return state
