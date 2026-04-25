from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.config import AppConfig
from src.hitl import escalate_case
from src.retriever import docs_to_context_and_citations, retrieve_context
from src.routing import decide_route, detect_intent, estimate_confidence
from src.schemas import GraphState


def _read_system_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "system_prompt.txt"
    return prompt_path.read_text(encoding="utf-8")


def _build_llm(config: AppConfig) -> ChatOpenAI:
    return ChatOpenAI(model=config.llm_model, api_key=config.openai_api_key, temperature=0)


def build_graph(config: AppConfig, vector_store, human_response_provider):
    system_prompt = _read_system_prompt()
    llm = _build_llm(config)

    def processing_node(state: GraphState) -> GraphState:
        query = state["query"]
        intent = detect_intent(query)

        docs = retrieve_context(query=query, vector_store=vector_store, k=config.top_k)
        contexts, citations = docs_to_context_and_citations(docs)
        context_block = "\n\n".join(contexts) if contexts else "No context found."

        answer = llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(
                    content=(
                        f"User query: {query}\n\n"
                        f"Retrieved context:\n{context_block}\n\n"
                        "Generate a grounded customer support response."
                    )
                ),
            ]
        ).content

        confidence = estimate_confidence(answer=answer, contexts=contexts)
        route = decide_route(
            intent=intent,
            confidence=confidence,
            contexts=contexts,
            threshold=config.confidence_threshold,
        )

        state["intent"] = intent
        state["contexts"] = contexts
        state["citations"] = citations
        state["draft_answer"] = answer
        state["confidence"] = confidence
        state["route"] = route
        state["escalated"] = False
        return state

    def output_node(state: GraphState) -> GraphState:
        if state.get("route") == "escalate":
            state = escalate_case(state, human_response_provider=human_response_provider)
        else:
            state["final_answer"] = state.get("draft_answer", "")
        return state

    def route_after_processing(state: GraphState) -> str:
        return state.get("route", "answer")

    workflow = StateGraph(GraphState)
    workflow.add_node("processing_node", processing_node)
    workflow.add_node("output_node", output_node)

    workflow.add_edge(START, "processing_node")
    workflow.add_conditional_edges(
        "processing_node",
        route_after_processing,
        {
            "answer": "output_node",
            "escalate": "output_node",
        },
    )
    workflow.add_edge("output_node", END)

    return workflow.compile()
