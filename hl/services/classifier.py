"""HL Classifier — validates and normalizes decision types."""

from hl.models import Decision

VALID_TYPES = ["approach", "architecture", "scope", "tool", "constraint", "other"]


def classify(decision: Decision) -> Decision:
    if decision.type not in VALID_TYPES:
        decision.type = "other"
    return decision


def classify_batch(decisions: list[Decision]) -> list[Decision]:
    return [classify(d) for d in decisions]
