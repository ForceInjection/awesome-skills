---
name: agent-skill-reviewer
description: Review Agent Skill directories and SKILL.md files against best practices. Use this skill when the user wants to review, validate, or check an Agent Skill implementation.
---

# Agent Skill Reviewer

## Instructions

When the user asks you to review an Agent Skill, follow these steps to ensure the skill complies with the best practices.

### 1. Identify the Target

Determine the directory path of the Agent Skill to be reviewed. Read the directory structure and the content of the `SKILL.md` file.

### 2. Analyze Directory Structure

Check if the project follows the production-grade directory structure:

- **Directory Name**: Must use `kebab-case`.
- **Core File**: Ensure the core instruction file is named exactly `SKILL.md` (uppercase).
- **Separation of Concerns**: Look for proper subdirectories (e.g., `scripts/` for executable code, `references/` for docs, `assets/` for static files).

### 3. Review Naming Conventions

- **Role-based Naming**: Check if the skill name uses a **Noun/Doer** format instead of a Verb/Action format (e.g., `agent-skill-reviewer` instead of `agent-skill-review`).

### 4. Review Frontmatter (Metadata Layer)

- Read the YAML frontmatter of `SKILL.md`.
- **Name**: Verify that the `name` field is present and matches the directory name.
- **Description Formula**: Verify that the `description` follows the golden formula: `[Function] + [Trigger Scenario] + [Keywords]`. It must be specific enough for the LLM to reason about when to trigger the skill.

### 5. Review Instructions (Core Logic Layer)

- **Clarity**: Check if the instructions are clear, step-by-step, and easy for an LLM to follow.
- **State & Concurrency**: Ensure the skill does not attempt to handle highly concurrent parallel tasks within a single conversation thread, as skills modify the context state.
- **Offloading**: Ensure no complex logic is hardcoded in Markdown if it can be offloaded to an external tool or script (e.g., in `scripts/`).
- **Progressive Disclosure**: Verify that detailed supplementary knowledge is placed in `references/` rather than cluttering the main `SKILL.md`.

### 6. Report Findings

Present a structured review report to the user using the following format:

- **Directory Structure & Naming**: Pass/Fail with details.
- **Frontmatter**: Pass/Fail with details.
- **Instructions**: Pass/Fail with details.
- **Recommendations**: Provide actionable recommendations for any violations of best practices.
