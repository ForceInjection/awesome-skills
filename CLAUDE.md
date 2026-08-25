# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a curated collection of 18 Agent Skills maintained by the "Force Injection" (原力注入) blogger. It is **not** a traditional software application — there is no build step, no runtime, and no compilation. Each skill is a self-contained directory with a `SKILL.md` instruction file that AI coding agents (Claude Code, Trae, Cursor, Qoder, OpenCode) load on demand to gain specialized capabilities.

Documentation is bilingual: `README.md`/`README-en.md` are the user-facing catalogs (Chinese and English), and `AGENTS.md`/`AGENTS-en.md` are the narrative project overviews. See the language conventions below.

## Commands

```bash
# Sync all skills to Claude Code (~/.claude/skills), Trae, and Qoder skill directories
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

```text
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

### Bilingual convention

Every Chinese-facing document has an English counterpart named with a `-en` suffix, and vice versa (`README.md` ↔ `README-en.md`, `SKILL.md` ↔ `SKILL-en.md`, `docs/gstack-deep-dive.md` ↔ `docs/gstack-deep-dive-en.md`):

- **Chinese skills ship a `SKILL-en.md`** next to the Chinese original, and the Chinese `SKILL.md` links to it via `> English version: [SKILL-en.md](SKILL-en.md)`. References that `SKILL-en.md` actually loads (e.g., review rules) also need `-en` counterparts with the `SKILL-en.md` paths updated to point at them.
- **Language alignment**: Chinese documents link to Chinese documents, English documents link to English documents. Cross-language links appear only as top-of-document language switchers (`[English](README-en.md) | **中文**`).
- **Deliberate exceptions** (do not translate): `editorial-card-designer/references/editorial-card-prompt.md` (intentionally Chinese-facing), CJK typography examples inside review rules, and example/template materials under `examples/` and `templates/`.

### Progressive disclosure

Skills use a three-layer loading strategy to avoid context overflow:

1. **Metadata layer** (always loaded): Skill name + description only.
2. **Core instruction layer** (loaded on trigger): Full `SKILL.md` body.
3. **Reference layer** (loaded as needed): Files in `references/`.

### Testing pyramid

The `unit-test/` framework has two layers:

1. **Static tests** (`unit-test/tests/run_static.py`): No LLM dependency. Validates link formats, image paths, naming conventions, and sensitive info sanitization. These are CI must-pass items. Currently only `doc-reviewer` and `md-translator` have static checks; other skills print a warning and exit 0.
2. **End-to-end tests** (`unit-test/opencode-skill-eval.sh`): Runs the skill through OpenCode CLI, captures JSONL event traces, and asserts behavior (tool call sequences, output artifacts, token usage). The pipeline writes artifacts to `unit-test/evals/artifacts/<skill-name>.jsonl` and reports to `unit-test/evals/reports/<skill-name>/`. The authoritative guide for writing and running eval tests is `unit-test/skill-eval-minimal-guide-en.md` (English; the Chinese original is `unit-test/skill-eval-minimal-guide.md`).

Test fixtures live in `unit-test/fixtures/<skill-name>/`, per-skill configs in `unit-test/skills/<skill-name>/config.sh`, and static check rules in `unit-test/tests/<skill-name>/checks.py`.

### Naming conventions

- Skill directories use **noun/doer form** in kebab-case: `agent-skill-reviewer` not `agent-skill-review`, `pdf-translator` not `translate-pdf`.
- This aligns with skills being "personified" agent roles.

### Key design principle: SKILL over Agent

The `code-reader` and `project-analyzer` skills output `SKILL.md` files rather than creating persistent agents. This keeps things decoupled and lightweight — any generic agent can load a skill file on demand to gain module-specific knowledge, avoiding role proliferation.

### Supporting directories

- **`docs/`**: Deep-dive analysis articles (`gstack-deep-dive.md`, `google-skill-patern.md`, `superpowers-deep-dive.md`, each with a `-en` English counterpart) — educational content about Agent Skill design patterns, not skills themselves.
- **`examples/`**: End-to-end usage examples for skills that produce visual or rendered output. Currently hosts `editorial-card-designer` examples (HTML source + rendered PNG). New skills with visual output should follow this pattern.

### Adding a new skill

1. Create `skills/<kebab-case-noun-doer>/` (e.g. `pdf-translator`, not `translate-pdf`) with `SKILL.md` (filename MUST be uppercase) plus `scripts/` and `references/` as needed.
2. `SKILL.md` starts with YAML frontmatter; `description` follows **[Function] + [Trigger Scenario] + [Keywords]** — it is the sole trigger mechanism.
3. Write `SKILL.md` in English by default; Chinese only when the target domain requires it (as with `dir-organizer` and `doc-reviewer`). Chinese skills must also ship a `SKILL-en.md` and link it from the Chinese `SKILL.md` (see the bilingual convention above).
4. Register the skill in four places: the README.md §1 table, the README-en.md §1 table, and the skill matrices in AGENTS.md and AGENTS-en.md.
5. If the skill needs testing, add fixtures to `unit-test/fixtures/<skill-name>/`, a config to `unit-test/skills/<skill-name>/config.sh`, and static checks to `unit-test/tests/<skill-name>/checks.py` wired into `run_static.py`.
6. Visual-output skills should also deposit a rendered example in `examples/`.
7. Run `bash ./sync.sh` to propagate the skill to `~/.claude/skills`, `~/.trae/skills`, and `~/.qoder/skills` (this is the standard local distribution mechanism).
