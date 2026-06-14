# Model Configuration
MODEL_NAME = "gemini-2.5-flash"

# Message Templates
ESCALATION_MESSAGE = (
    "Unable to confidently answer using available documentation. "
    "Escalating to human support."
)

INJECTION_MESSAGE = (
    "This request appears to be attempting to access internal "
    "system information and cannot be processed."
)

HUMAN_REVIEW_MESSAGE = (
    "This issue requires review by a human support specialist."
)

# Confidence Threshold
MIN_CONFIDENCE = 75  # Escalate if below this
