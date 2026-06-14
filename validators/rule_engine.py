def apply_rules(ticket: str):
    ticket = ticket.strip()

    if not ticket:
        return {
            "handled": True,
            "response": "Please provide details about your issue."
        }

    if ticket.lower() in ["thanks", "thank you", "ok", "okay"]:
        return {
            "handled": True,
            "response": "You're welcome!"
        }

    return {
        "handled": False,
        "response": None
    }