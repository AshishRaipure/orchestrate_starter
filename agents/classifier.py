def classify_ticket(ticket: str):

    text = ticket.lower()

    if any(word in text for word in ["password", "login", "sign in", "account"]):
        return "ACCOUNT"

    if any(word in text for word in ["refund", "charge", "payment", "billing"]):
        return "BILLING"

    if any(word in text for word in ["blocked card", "stolen card", "fraud"]):
        return "FRAUD"

    if any(word in text for word in ["error", "bug", "crash", "not loading"]):
        return "TECHNICAL"

    return "UNKNOWN"