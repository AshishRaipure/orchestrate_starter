import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent.log")


def ensure_log_dir():
    """Create logs directory if it doesn't exist."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log_event(event: str):
    """
    Log an event to the audit log.
    
    Args:
        event: Event string to log
    """
    ensure_log_dir()
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {event}\n")
