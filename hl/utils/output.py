"""
HL Terminal Output
ANSI-based formatting. No external dependencies.
"""

# ANSI codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"


def c(text: str, *styles: str) -> str:
    """Wrap text with ANSI styles."""
    return "".join(styles) + str(text) + RESET


def panel(content: str, title: str = "", color: str = WHITE, width: int = 70) -> str:
    """Render a bordered panel."""
    border = color
    lines = []
    top = f"{border}┌{'─' * (width - 2)}┐{RESET}"
    bot = f"{border}└{'─' * (width - 2)}┘{RESET}"

    if title:
        pad = width - 4 - len(_strip_ansi(title))
        top = f"{border}┌─ {title} {'─' * max(0, pad)}┐{RESET}"

    lines.append(top)
    for line in content.split("\n"):
        visible_len = len(_strip_ansi(line))
        padding = max(0, width - 4 - visible_len)
        lines.append(f"{border}│{RESET} {line}{' ' * padding} {border}│{RESET}")
    lines.append(bot)
    return "\n".join(lines)


def rule(label: str = "", width: int = 70, color: str = DIM) -> str:
    """Render a horizontal rule."""
    if label:
        pad = width - len(label) - 2
        return f"{color}{'─' * 1} {label} {'─' * max(0, pad - 1)}{RESET}"
    return f"{color}{'─' * width}{RESET}"


def table(headers: list[str], rows: list[list[str]], col_widths: list[int] | None = None) -> str:
    """Render a simple table."""
    if not rows:
        return ""

    if col_widths is None:
        col_widths = [
            max(len(_strip_ansi(str(r[i]))) for r in [headers] + rows) + 2
            for i in range(len(headers))
        ]

    def fmt_row(cells, widths, bold=False):
        parts = []
        for cell, w in zip(cells, widths):
            visible = _strip_ansi(str(cell))
            pad = max(0, w - len(visible))
            parts.append(str(cell) + " " * pad)
        style = BOLD if bold else ""
        return f"{style}  {'  '.join(parts)}{RESET}"

    lines = []
    lines.append(fmt_row([c(h, DIM) for h in headers], col_widths, bold=True))
    lines.append(f"  {DIM}{'  '.join('─' * w for w in col_widths)}{RESET}")
    for row in rows:
        lines.append(fmt_row(row, col_widths))
    return "\n".join(lines)


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    import re
    return re.sub(r"\033\[[0-9;]*m", "", text)
