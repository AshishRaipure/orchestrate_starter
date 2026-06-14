from pathlib import Path

DOC_MAP = {
    "ACCOUNT": "password_reset.txt",
    "BILLING": "refund_policy.txt",
    "TECHNICAL": "technical_support.txt"
}

_FULL_PATHS = {
    "ACCOUNT": "data/password_reset.txt",
    "BILLING": "data/refund_policy.txt",
    "TECHNICAL": "data/technical_support.txt"
}


def retrieve_document(category):

    path = _FULL_PATHS.get(category)

    if not path:
        return None

    return Path(path).read_text(encoding="utf-8")