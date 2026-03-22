"""hl init — Initialize Hidden Layer in the current project."""

import click
from hl.db import init_db, db_exists
from hl.config import DB_PATH
from hl.utils.output import panel, c, GREEN, CYAN, WHITE, DIM, BOLD, YELLOW


def init_command():
    """Initialize HL in the current project directory."""

    if db_exists():
        print()
        print(panel(
            f"  {c('HL already initialized in this project.', YELLOW)}\n"
            f"  {c(f'Database: {DB_PATH}', DIM)}",
            title=c(" ⚠  Already initialized ", YELLOW),
            color=YELLOW,
        ))
        print()
        raise click.exceptions.Exit()

    init_db()

    print()
    print(panel(
        f"  {c('Hidden Layer initialized.', BOLD)}\n\n"
        f"  {c('Database:  ', DIM)}{c(str(DB_PATH), CYAN)}\n"
        f"  {c('Status:    ', DIM)}{c('ready', GREEN)}\n\n"
        f"  {c('Next step: ', DIM)}run {c('hl snap', CYAN + BOLD)} after your next AI session.",
        title=c(" ✓  HL initialized ", GREEN),
        color=GREEN,
    ))
    print()
