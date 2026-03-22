"""hl snap — Capture decisions from the current AI session."""

import click
from hl.db import insert_decision, db_exists
from hl.models import Decision
from hl.services.detector import detect_decisions
from hl.services.classifier import classify_batch
from hl.utils.helpers import generate_session_id
from hl.utils.output import panel, table, c, GREEN, CYAN, YELLOW, RED, MAGENTA, BLUE, DIM, BOLD, WHITE

TYPE_COLORS = {
    "architecture": CYAN,
    "scope":        YELLOW,
    "tool":         MAGENTA,
    "approach":     BLUE,
    "constraint":   RED,
    "other":        WHITE,
}


def snap_command():
    """Process the current session and capture decisions."""

    if not db_exists():
        print(c("  ✗ HL not initialized. Run 'hl init' first.", RED))
        raise click.exceptions.Exit(1)

    session_id = generate_session_id()

    print()
    print(c("  Scanning session for decisions...", DIM))
    print()

    candidates = classify_batch(detect_decisions(session_id=session_id))

    if not candidates:
        print(c("  No decisions detected in this session.", YELLOW))
        raise click.exceptions.Exit()

    # Build table rows
    rows = []
    for i, d in enumerate(candidates, 1):
        color = TYPE_COLORS.get(d.type, WHITE)
        rows.append([
            c(str(i), DIM),
            d.content,
            c(d.type, color),
            c(d.reason or "—", DIM),
        ])

    output = table(
        headers=["#", "Decision", "Type", "Reason"],
        rows=rows,
        col_widths=[3, 44, 14, 30],
    )

    print(panel(
        "\n" + output + "\n",
        title=c(f" Decisions detected — {len(candidates)} found ", WHITE),
        color=BLUE,
    ))

    print()
    confirm = click.confirm("  Save these decisions?", default=True)

    if not confirm:
        print()
        print(c("  Skipped. Nothing was saved.", DIM))
        print()
        raise click.exceptions.Exit()

    for d in candidates:
        d.status = "confirmed"
        insert_decision(
            id=d.id,
            content=d.content,
            type=d.type,
            session_id=d.session_id,
            reason=d.reason,
            status="confirmed",
        )

    print()
    print(panel(
        f"  {c(f'{len(candidates)} decision(s) saved.', BOLD)}\n\n"
        f"  Run {c('hl resume', CYAN + BOLD)} to see the full project state.",
        title=c(" ✓  Snapshot saved ", GREEN),
        color=GREEN,
    ))
    print()
