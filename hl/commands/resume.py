"""hl resume — Show current project state."""

import click
from hl.db import list_decisions, db_exists
from hl.utils.helpers import format_date
from hl.utils.output import panel, c, GREEN, CYAN, YELLOW, RED, MAGENTA, BLUE, DIM, BOLD, WHITE

TYPE_ICONS = {
    "architecture": ("◆", CYAN),
    "scope":        ("◎", YELLOW),
    "tool":         ("⬡", MAGENTA),
    "approach":     ("→", BLUE),
    "constraint":   ("⊘", RED),
    "other":        ("·", WHITE),
}


def resume_command():
    """Display current project state — all confirmed decisions."""

    if not db_exists():
        print(c("  ✗ HL not initialized. Run 'hl init' first.", RED))
        raise click.exceptions.Exit(1)

    decisions = list_decisions(status="confirmed")

    print()

    if not decisions:
        print(panel(
            f"  {c('No confirmed decisions yet.', DIM)}\n\n"
            f"  Run {c('hl snap', CYAN + BOLD)} after your next AI session.",
            title=c(" Project State ", WHITE),
            color=WHITE,
        ))
        print()
        return

    lines = ""
    for d in decisions:
        icon, color = TYPE_ICONS.get(d["type"], ("·", WHITE))
        date = format_date(d["created_at"])
        lines += f"  {c(icon, color)}  {d['content']}"
        lines += f"  {c(date, DIM)}\n"
        if d["reason"]:
            lines += f"     {c(d['reason'], DIM)}\n"
        lines += "\n"

    print(panel(
        "\n" + lines.rstrip(),
        title=c(f" Project State  {DIM}({len(decisions)} decisions){WHITE} ", WHITE),
        color=WHITE,
    ))

    # Legend
    legend = "  "
    for type_name, (icon, color) in TYPE_ICONS.items():
        legend += c(f"{icon} {type_name}", color) + "   "
    print(c(legend, DIM))
    print()
