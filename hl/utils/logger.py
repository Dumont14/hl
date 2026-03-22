"""HL Logger — simple structured prints."""

import os
from hl.utils.output import c, GREEN, YELLOW, RED, DIM

DEBUG = os.getenv("HL_DEBUG", "false").lower() == "true"


def info(msg: str)    -> None: print(c(f"  {msg}", DIM))
def success(msg: str) -> None: print(c(f"  ✓ {msg}", GREEN))
def warning(msg: str) -> None: print(c(f"  ⚠ {msg}", YELLOW))
def error(msg: str)   -> None: print(c(f"  ✗ {msg}", RED))
def debug(msg: str)   -> None:
    if DEBUG:
        import sys
        print(c(f"[DEBUG] {msg}", DIM), file=sys.stderr)
