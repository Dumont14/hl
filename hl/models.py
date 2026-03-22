"""HL Data Models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

DecisionType   = Literal["approach", "architecture", "scope", "tool", "constraint", "other"]
DecisionStatus = Literal["pending", "confirmed", "revoked"]


@dataclass
class Decision:
    id: str
    content: str
    type: DecisionType    = "approach"
    status: DecisionStatus = "pending"
    reason: str           = ""
    session_id: str       = ""
    created_at: str       = field(default_factory=lambda: datetime.now().isoformat())
    revoked_at: str | None = None
