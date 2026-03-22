"""HL Helpers — general-purpose utilities."""

import uuid
from datetime import datetime


def generate_session_id() -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"session_{ts}_{str(uuid.uuid4())[:8]}"


def format_date(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).strftime("%d %b")
    except Exception:
        return "—"


def truncate(text: str, n: int = 60) -> str:
    return text if len(text) <= n else text[:n - 3] + "..."
