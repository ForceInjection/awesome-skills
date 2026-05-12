# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a curated collection of 17 Agent Skills maintained by the "Force Injection" (原力注入) blogger. It is **not** a traditional software application — there is no build step, no runtime, and no compilation. Each skill is a self-contained directory with a `SKILL.md` instruction file that AI coding agents (Claude Code, Trae, Cursor, Qoder, OpenCode) load on demand to gain specialized capabilities.

## Commands

```bash
# Sync all skills to Trae and Qoder skill directories
bash ./sync.sh

# Run static unit tests for a skill (no LLM needed)
python3 ./unit-test/tests/run_static.py <skill-name>

# Run end-to-end evaluation for a skill (requires OpenCode CLI + LLM API key)
SKILL=<skill-name> bash ./unit-test/opencode-skill-eval.sh all

# Run behavior assertions against evaluation artifacts
SKILL=<skill-name> node ./unit-test/evals/agent/checks.js \
  ./unit-test/evals/artifacts/<skill-name>.jsonl \
  ./unit-test/evals/reports/<skill-name>
```

## Architecture

### Skill structure

Every skill follows this standard directory layout:

```
skill-name/
├── SKILL.md       # Core instruction file (filename MUST be uppercase)
├── scripts/       # Executable scripts (Python, Shell)
├── references/    # Supplementary documents loaded on demand
└── assets/        # Static resources (images, templates)
```

Each `SKILL.md` starts with YAML frontmatter. The `description` field is the sole trigger mechanism — agents use it to decide whether to load the skill. Follow the formula: **"[Function] + [Trigger Scenario] + [Keywords]"**.

### Language conventions (audience isolation)

- **Agent-facing files** (`SKILL.md`, prompt templates): English — maximizes LLM instruction-following accuracy.
- **Human-facing deliverables** (reports, generated docs): Chinese, with professional formatting rules (e.g., spaces between Chinese and English).
- **Exception**: Skills like `dir-organizer` and `doc-reviewer` use Chinese in `SKILL.md` because their target domain (Chinese doc standards, directory planning) requires precise Chinese instructions.

### Progressive disclosure

Skills use a three-layer loading strategy to avoid context overflow:
1. **Metadata layer** (always loaded): Skill name + description only.
2. **Core instruction layer** (loaded on trigger): Full `SKILL.md` body.
3. **Reference layer** (loaded as needed): Files in `references/`.

### Testing pyramid

The `unit-test/` framework has two layers:

1. **Static tests** (`unit-test/tests/run_static.py`): No LLM dependency. Validates link formats, image paths, naming conventions, and sensitive info sanitization. These are CI must-pass items.
2. **End-to-end tests** (`unit-test/opencode-skill-eval.sh`): Runs the skill through OpenCode CLI, captures JSONL event traces, and asserts behavior (tool call sequences, output artifacts, token usage).

Test fixtures live in `unit-test/fixtures/<skill-name>/`, per-skill configs in `unit-test/skills/<skill-name>/config.sh`, and static check rules in `unit-test/tests/<skill-name>/checks.py`.

### Naming conventions

- Skill directories use **noun/doer form** in kebab-case: `agent-skill-reviewer` not `agent-skill-review`, `pdf-translator` not `translate-pdf`.
- This aligns with skills being "personified" agent roles.

### Key design principle: SKILL over Agent

The `code-reader` and `project-analyzer` skills output `SKILL.md` files rather than creating persistent agents. This keeps things decoupled and lightweight — any generic agent can load a skill file on demand to gain module-specific knowledge, avoiding role proliferation.
