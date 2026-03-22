"""
HL — Hidden Layer
State infrastructure for AI workflows.
"""

import click
from hl.commands.init import init_command
from hl.commands.snap import snap_command
from hl.commands.resume import resume_command
from hl.commands.context import context_command


@click.group()
def app():
    """HL — Hidden Layer. State infrastructure for AI workflows."""
    pass


app.command("init",    help="Initialize HL in the current project.")(init_command)
app.command("snap",    help="Capture decisions from the current session.")(snap_command)
app.command("resume",  help="Show current project state.")(resume_command)
app.command("context", help="Preview the context block for the next prompt.")(context_command)


if __name__ == "__main__":
    app()
