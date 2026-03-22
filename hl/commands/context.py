"""hl context — Preview the context block that HL would inject."""

import click
from hl.db import get_recent_decisions, db_exists
from hl.services.context_manager import build_context_block
from hl.config import MAX_CONTEXT_DECISIONS
from hl.utils.output import panel, c, CYAN, DIM, WHITE, BOLD


def context_command():
    """Preview the context block injected before each AI prompt."""

    if not db_exists():
        print(c("  ✗ HL not initialized. Run 'hl init' first.", "\033[31m"))
        raise click.exceptions.Exit(1)

    decisions = get_recent_decisions(limit=MAX_CONTEXT_DECISIONS)

    print()

    if not decisions:
        print(panel(
            f"  {c('No decisions to inject yet.', DIM)}\n\n"
            f"  Run {c('hl snap', CYAN + BOLD)} to capture your first decisions.",
            title=c(" Context Block ", WHITE),
            color=WHITE,
        ))
        print()
        return

    block = build_context_block(decisions)

    # Indent each line for display
    indented = "\n".join(f"  {line}" for line in block.split("\n"))

    print(panel(
        "\n" + indented + "\n",
        title=c(f" Context Block  {DIM}({len(decisions)} decisions · injected before each prompt){WHITE} ", WHITE),
        color=CYAN,
    ))

    print(c("  This block is prepended automatically to each new AI session.", DIM))
    print()
