# HL — Hidden Layer

**State infrastructure for AI workflows.**

HL captures the decisions made during AI-assisted development and makes them persistent — so you never have to reconstruct context again.

---

## The problem

Every time you start a new AI session, you start from zero. The model doesn't know what was decided, why a certain architecture was chosen, or what the next step was. You reconstruct that context manually. Every time.

HL fixes this.

---

## How it works

```
AI session → hl snap → decisions saved → hl resume → full context restored
```

A **decision** is any choice that changes the direction of the system and persists across steps.

HL captures those decisions, stores them locally in SQLite, and makes them available for your next session.

---

## What it feels like

**Without HL:**
You reopen a project after 4 days and spend 10 minutes reading old threads, grepping through code, trying to remember why you made that call.

**With HL:**

```
$ hl resume
```

```
Project State  (3 decisions)

◆  Use SQLite as local database — no external infra in MVP       22 Mar
   Avoids cloud dependency, ships faster, easy to migrate later

◎  Skip OAuth in v1 — email-only authentication                  22 Mar
   OAuth adds 2–3 days of complexity before validation

→  CLI-first interface before any web UI                         22 Mar
   Target audience lives in terminal. Validates core value faster.
```

In 10 seconds you know exactly where you were. No reconstruction. No archaeology.

---

## Example session

```
$ hl snap

  Scanning session for decisions...

  ┌─ Decisions detected — 3 found ──────────────────────────────┐
  │                                                              │
  │  #  Decision                              Type               │
  │  ─  ────────────────────────────────────  ────────────────   │
  │  1  Use SQLite — no external infra        architecture       │
  │  2  Skip OAuth in v1                      scope              │
  │  3  CLI-first before web UI               approach           │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  Save these decisions? [Y/n]: y

  ✓ 3 decision(s) saved.
```

---

## Install

```bash
git clone <repo>
cd hiddenlayer
pip install -r requirements.txt
```

Install as CLI tool:

```bash
pip install -e .
```

Or run directly:

```bash
PYTHONPATH=. python -m hl.main <command>
```

---

## Commands

### `hl init`
Initialize HL in the current project directory. Creates `.hl.db`.

```bash
hl init
```

### `hl snap`
Capture decisions from the current session. Presents detected decisions and asks for confirmation before saving.

```bash
hl snap
```

### `hl resume`
Show the current project state — all confirmed decisions with type, reason, and date.

```bash
hl resume
```

### `hl context`
Preview the context block that would be injected into your next AI prompt.

```bash
hl context
```

---

## Project structure

```
hl/
├── main.py              # CLI entrypoint
├── config.py            # Paths and env config
├── db.py                # SQLite layer
├── models.py            # Data structures
├── commands/
│   ├── init.py          # hl init
│   ├── snap.py          # hl snap
│   ├── resume.py        # hl resume
│   └── context.py       # hl context
├── services/
│   ├── detector.py      # Decision detection (V1: mock, V2: LLM)
│   ├── classifier.py    # Decision type validation
│   └── context_manager.py  # Context block builder
└── utils/
    ├── output.py        # ANSI terminal formatting
    ├── logger.py        # Structured log helpers
    └── helpers.py       # General utilities
```

---

## Decision types

HL automatically classifies decisions into the following categories:

| Icon | Type         | Meaning                          |
|------|--------------|----------------------------------|
| ◆    | architecture | Structural choices               |
| ◎    | scope        | What's in / out of the build     |
| ⬡    | tool         | Libraries, services, frameworks  |
| →    | approach     | How something will be done       |
| ⊘    | constraint   | Hard limits and non-negotiables  |
| ·    | other        | Everything else                  |

---

## Roadmap

| Version | What changes                                      |
|---------|---------------------------------------------------|
| V1      | Mock decisions, CLI validation, SQLite core       |
| V2      | Real LLM detection from session transcripts       |
| V3      | Auto-injection into Cursor / Claude sessions      |
| V4      | Multi-project sync across machines                |

---

## Config

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable                   | Default                  | Description                     |
|----------------------------|--------------------------|---------------------------------|
| `ANTHROPIC_API_KEY`        | —                        | Required in V2                  |
| `HL_LLM_MODEL`             | claude-sonnet-4-20250514 | Model for detection             |
| `HL_MAX_CONTEXT_DECISIONS` | 10                       | Max decisions per context block |
| `HL_DEBUG`                 | false                    | Debug output                    |

---

## Philosophy

- **Local-first.** Your decisions live in your repo, not in the cloud.
- **Explicit over implicit.** Every decision is visible, typed, and reasoned.
- **Minimal friction.** One lightweight checkpoint per session.
- **Invisible in production.** The context block does its job silently.

---

*Hidden Layer. The state your agent was missing.*
