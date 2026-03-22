"""HL Context Manager — builds the prompt injection block."""

import sqlite3


def build_context_block(decisions: list[sqlite3.Row]) -> str:
    """Build a markdown context block ready to inject into any AI prompt."""
    if not decisions:
        return ""

    lines = [
        "## [HL] Project Context",
        "Active decisions — treat these as established premises:\n",
    ]

    for d in decisions:
        line = f"- **{d['content']}**"
        if d["reason"]:
            line += f"  _{d['reason']}_"
        lines.append(line)

    lines.append(
        "\n_Context injected by Hidden Layer. Do not contradict unless explicitly asked._"
    )

    return "\n".join(lines)
