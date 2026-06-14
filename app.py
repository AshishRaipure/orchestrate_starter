import os
from dotenv import load_dotenv
from google import genai
from safety.injection_detector import detect_prompt_injection
from validators.rule_engine import apply_rules
from agents.classifier import classify_ticket
from retrieval.retriever import retrieve_document, DOC_MAP
from config import (
    MODEL_NAME,
    ESCALATION_MESSAGE,
    INJECTION_MESSAGE,
    HUMAN_REVIEW_MESSAGE,
    MIN_CONFIDENCE,
)
from audit import log_event, ensure_log_dir

# Initialize logging
ensure_log_dir()

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# -----------------------------
# Configure Gemini
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# Terminal UI
# -----------------------------
print("=" * 50)
print("Orchestrate Starter Agent")
print("Type 'exit' to quit")
print("=" * 50)

while True:

    ticket = input("\nSupport Ticket: ")

    # Exit Condition (check first)
    if ticket.lower() == "exit":
        print("\nGoodbye!")
        break

    log_event(f"TICKET={ticket}")

    if detect_prompt_injection(ticket):
        log_event(f"ACTION=INJECTION_BLOCKED")
        print("\nResponse:")
        print(INJECTION_MESSAGE)
        continue

    # -----------------------------
    # Rule Engine
    # -----------------------------
    rule_result = apply_rules(ticket)

    if rule_result["handled"]:
        log_event(f"ACTION=RULE_ENGINE_HIT")
        print("\nResponse:")
        print(rule_result["response"])
        continue


    # NEW: Ticket Classification
    category = classify_ticket(ticket)
    log_event(f"CATEGORY={category}")

    print(f"\n[Category: {category}]")

    document = retrieve_document(category)

    # Check if document exists
    if document is None:
        log_event(f"ACTION=NO_DOCUMENT_AVAILABLE")
        print("\nResponse:")
        print(HUMAN_REVIEW_MESSAGE)
        continue

    # -----------------------------
    # Gemini Processing
    # -----------------------------
    try:

        prompt = f"""You are a support triage assistant.

You MUST answer ONLY using the supplied support document.

If the answer cannot be found in the document,
respond with exactly:

ESCALATE

Always include your confidence score (0-100) in your response format:

CONFIDENCE: <score>
ANSWER: <your response>

Support Document:
{document}

Customer Ticket:
{ticket}
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        response_text = response.text.strip()
        
        # Parse confidence and answer
        confidence = 0
        answer = response_text
        
        if "CONFIDENCE:" in response_text:
            try:
                lines = response_text.split("\n")
                for i, line in enumerate(lines):
                    if "CONFIDENCE:" in line:
                        confidence = int(line.split(":")[1].strip())
                    elif "ANSWER:" in line:
                        answer = "\n".join(lines[i+1:])
                        break
            except (ValueError, IndexError):
                confidence = 0
        
        log_event(f"CONFIDENCE={confidence}")

        if response_text == "ESCALATE" or confidence < MIN_CONFIDENCE:
            log_event(f"ACTION=ESCALATION")
            print("\nResponse:")
            print(ESCALATION_MESSAGE)
        else:
            log_event(f"ACTION=RESPONSE_PROVIDED|SOURCE={DOC_MAP[category]}")
            print("\nResponse:")
            print(answer)
            print(f"\nConfidence: {confidence}%")
            print(f"Source: {DOC_MAP[category]}")

    except Exception as e:
        print("\nError:")
        print(str(e))