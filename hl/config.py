"""HL Configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT        = Path(os.getenv("HL_PROJECT_ROOT", Path.cwd()))
DB_PATH             = PROJECT_ROOT / ".hl.db"
LLM_PROVIDER        = os.getenv("HL_LLM_PROVIDER", "anthropic")
LLM_MODEL           = os.getenv("HL_LLM_MODEL", "claude-sonnet-4-20250514")
ANTHROPIC_API_KEY   = os.getenv("ANTHROPIC_API_KEY", "")
MAX_CONTEXT_DECISIONS = int(os.getenv("HL_MAX_CONTEXT_DECISIONS", "10"))
