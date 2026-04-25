SENSITIVE_KEYWORDS = {
    "legal",
    "lawsuit",
    "complaint",
    "chargeback",
    "fraud",
    "threat",
    "breach",
}

COMPLEX_KEYWORDS = {
    "refund",
    "escalate",
    "manager",
    "urgent",
    "security",
    "locked",
    "double charged",
}


def detect_intent(query: str) -> str:
    lower_q = query.lower()
    if any(word in lower_q for word in SENSITIVE_KEYWORDS):
        return "sensitive"
    if any(word in lower_q for word in COMPLEX_KEYWORDS):
        return "complex"
    return "faq"


def estimate_confidence(answer: str, contexts: list[str]) -> float:
    if not contexts:
        return 0.1

    weak_answer_markers = [
        "i don't know",
        "not sure",
        "cannot find",
        "insufficient",
        "not available",
    ]

    lower_ans = answer.lower()
    if any(marker in lower_ans for marker in weak_answer_markers):
        return 0.3

    # Heuristic confidence: has context + answer has usable length.
    if len(answer.strip()) > 80:
        return 0.82
    return 0.68


def decide_route(
    intent: str,
    confidence: float,
    contexts: list[str],
    threshold: float,
) -> str:
    if intent in {"sensitive", "complex"}:
        return "escalate"
    if not contexts:
        return "escalate"
    if confidence < threshold:
        return "escalate"
    return "answer"
