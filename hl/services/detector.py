"""
HL Decision Detector
V1: Mock decisions for CLI validation.
V2: LLM extraction from session transcripts.
"""

import uuid
from hl.models import Decision
from hl.utils.helpers import generate_session_id

MOCK_DECISIONS = [
    {
        "content": "Use SQLite as local database — no external infra in MVP",
        "type": "architecture",
        "reason": "Avoids cloud dependency, ships faster, easy to migrate later",
    },
    {
        "content": "Skip OAuth in v1 — email-only authentication",
        "type": "scope",
        "reason": "OAuth adds 2–3 days of complexity before validation",
    },
    {
        "content": "CLI-first interface before any web UI",
        "type": "approach",
        "reason": "Target audience lives in terminal. Validates core value faster.",
    },
]


def detect_decisions(session_id: str | None = None) -> list[Decision]:
    """
    V1: Returns mock decisions.
    V2: Will accept a transcript and call LLM for real extraction.
    """
    if session_id is None:
        session_id = generate_session_id()

    return [
        Decision(
            id=str(uuid.uuid4()),
            content=m["content"],
            type=m["type"],
            reason=m.get("reason", ""),
            session_id=session_id,
            status="pending",
        )
        for m in MOCK_DECISIONS
    ]


# --- V2 PLACEHOLDER ---
# def detect_from_transcript(transcript: str, session_id: str) -> list[Decision]:
#     """Call LLM to extract decisions from raw session transcript."""
#     pass
