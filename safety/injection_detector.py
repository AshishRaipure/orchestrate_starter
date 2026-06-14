INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal system prompt",
    "show system prompt",
    "display system prompt",
    "show hidden prompt",
    "developer message",
    "internal instructions",
    "show internal documents",
    "reveal internal documents",
    "print your prompt",
    "what are your instructions",
]


def detect_prompt_injection(ticket: str):
    text = ticket.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in text:
            return True

    return False