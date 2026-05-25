# Agent Skill Best Practices Reference

## Production-Grade Directory Structure

```
skill-name/
├── SKILL.md       # Core instruction file (filename MUST be uppercase)
├── scripts/       # Executable scripts (Python, Shell)
├── references/    # Supplementary documents loaded on demand
└── assets/        # Static resources (images, templates)
```

## Trigger Description Formula

The `description` field in YAML frontmatter must follow: **[Function] + [Trigger Scenario] + [Keywords]**

Example: "Review Agent Skill directories and SKILL.md files against best practices. Use this skill when the user wants to review, validate, or check an Agent Skill implementation."

## Naming Conventions

- Use **Noun/Doer** form: `agent-skill-reviewer` not `agent-skill-review`
- Use **kebab-case** for multi-word names
- `SKILL.md` filename must be uppercase

## Progressive Disclosure

Three-layer loading strategy:
1. Metadata layer (always loaded): name + description
2. Core instruction layer (loaded on trigger): full SKILL.md body
3. Reference layer (loaded as needed): files in references/

## Language Conventions

- Agent-facing files (SKILL.md, prompts): English
- Human-facing deliverables (reports, docs): Chinese
- Exception: Chinese SKILL.md for skills targeting Chinese doc standards
