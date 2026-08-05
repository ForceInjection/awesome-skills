# Awesome Agent Skills

[中文](README.md) | **English**

A curated collection of production-grade Agent Skills maintained by the "Force Injection" (原力注入) blogger. These skills automate workflows and orchestrate multi-agent collaboration across code reading and architecture analysis, document processing and review, content creation and design, and spec-driven development — helping developers get more out of AI-assisted coding and automated operations.

## Table of Contents

- [1. Core Skills](#1-core-skills)
- [2. Core Design Principles](#2-core-design-principles)
- [3. Agent Skill Best Practices](#3-agent-skill-best-practices)
- [4. Deep Dive Case Studies](#4-deep-dive-case-studies)
- [5. Recommended Resources](#5-recommended-resources)
- [6. Skill Unit Testing](#6-skill-unit-testing)

---

## 1. Core Skills

To address engineering challenges such as unfamiliar codebases, project reverse engineering, and spec-driven development, this project packages **17 standalone agent skills** designed to solve real development bottlenecks through multi-role collaboration.

| Skill | What it does | Trigger |
|-------|--------------|---------|
| [`code-reader`](./skills/code-reader) | Deep code reading: three-agent collaboration (technical writer / QA engineer / junior developer) with a closed-book exam validation loop to systematically read unfamiliar codebases and produce reusable cognitive skills | `/code-reader <source> <output-dir>` |
| [`project-analyzer`](./skills/project-analyzer) | Deep project architecture analysis: builds on `code-reader` to reverse-engineer and statically analyze third-party repositories, producing an architecture deep-dive report with 7 standard sections (code analysis & execution flow ≈ 70% of the report) | `/project-analyzer <source> <output-dir>` |
| [`dir-organizer`](./skills/dir-organizer) | Directory organization: restructures project directories after printing the full plan for user approval, then auto-updates internal reference links | `/dir-organizer <target-dir>` |
| [`doc-reviewer`](./skills/doc-reviewer) | Document review: four independent review types (outline / content / assets & links / format) with rules loaded on demand; can auto-apply fixes with user authorization | `/doc-reviewer <target-file>` |
| [`md-summarizer`](./skills/md-summarizer) | Markdown summarizer: extracts core summary, deep analysis, and key takeaways; supports multi-file comparative analysis and outputs structured Chinese reports | `/md-summarizer <file...>` |
| [`update-submitter`](./skills/update-submitter) | Commit assistant: analyzes `git status`/`git diff`, groups related changes into logical units, generates Conventional Commits messages, and commits after user authorization | `/update-submitter <target-dir>` |
| [`agent-skill-reviewer`](./skills/agent-skill-reviewer) | Agent Skill reviewer: audits skill directory structure, YAML frontmatter (description formula), and instruction clarity; outputs a structured review report | `/agent-skill-reviewer <target-dir>` |
| [`openspec-assistant`](./skills/openspec-assistant) | OpenSpec spec-driven development: architect / developer / QA tri-role collaboration covering intent alignment, spec generation, code implementation, and automated verification; built-in `/opsx` command system | `/openspec-assistant [intent]` |
| [`web-content-downloader`](./skills/web-content-downloader) | Web content downloader: Jina Reader body extraction + smart download and rename of key images + HTML table → Markdown conversion, preserving the original language | `/web-content-downloader <URL>` |
| [`md-translator`](./skills/md-translator) | Markdown translator: translates to a target language (Chinese by default), strictly preserving Markdown formatting, with built-in typography checks (e.g., spaces between CJK and Latin) | `/md-translator <target-file>` |
| [`reference-organizer`](./skills/reference-organizer) | Citation organizer: three fetching channels (arXiv API / Crossref DOI / headless browser) producing citations in GB/T 7714 / APA / IEEE formats | `/reference-organizer [URL/DOI/ID]` |
| [`md-link-checker`](./skills/md-link-checker) | Markdown link checker: multi-threaded scanning with LRU cache validates local and external links; parses HTML image tags | `/md-link-checker <target-file\|dir>` |
| [`drawio-designer`](./skills/drawio-designer) | Draw.io diagram designer: operates on `.drawio` XML directly with AWS icon mapping and overlap-avoidance routing rules; exports transparent high-resolution PNGs headlessly | `/drawio-designer <diagram-file>` |
| [`pptx-reader`](./skills/pptx-reader) | PPTX reader: markitdown text extraction + XML unpacking + lossless LibreOffice/Poppler rendering to high-resolution images; runs in an isolated Python venv | `/pptx-reader <target-file>` |
| [`ontology`](./skills/ontology) | Typed knowledge graph: 16 entity / 15 relation types with property, cardinality, and cycle constraint validation; append-only JSONL event log for auditability; serves as a memory base for cross-skill state sharing | `python3 scripts/ontology.py <cmd>` |
| [`editorial-card-designer`](./skills/editorial-card-designer) | Editorial info cards: high-density HTML cards in modern magazine + Swiss International Typographic Style, 8 fixed aspect-ratio presets, headless Chrome renders pixel-aligned PNG screenshots | conversational workflow |
| [`tech-outline-planner`](./skills/tech-outline-planner) | Technical article outline planning: combined narrative structure (Context-first + Process narrative) following the given-before-new cognitive principle, producing "architecture-review-grade" outlines | `/tech-outline-planner [topic/problem/draft]` |

> Provenance: `ontology` is imported from [hanzoskill/ontology](https://github.com/hanzoskill/ontology) (locally enhanced superset), `editorial-card-designer` is imported from [shaom/infocard-skills](https://github.com/shaom/infocard-skills) (renamed & hardened locally), and `pptx-reader` is based on [anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md). Full usage examples and end-to-end demos live in each skill's `SKILL.md` and the `examples/` directory.

---

## 2. Core Design Principles

To maximize LLM reasoning effectiveness and the developer reading experience, this project enforces strict standards on **audience isolation** (bilingual EN/CN layering) and decoupled lightweight design.

### 2.1 Language Convention: Audience Isolation

- **Agent/LLM-facing files (English only)**: All `SKILL.md` files consumed as external knowledge by agents, and `*-prompt.md` workflow templates, are written in English to maximize instruction-following accuracy.
- **Human-facing deliverables (Chinese only)**: Reports delivered to developers (e.g., the architecture deep-dive report generated by `project-analyzer`) are produced in Chinese with professional typography (e.g., spaces between CJK and Latin text).

**Exception (Chinese skill docs)**: Skills such as `dir-organizer` and `doc-reviewer` use Chinese in their `SKILL.md`. Their core goal is guiding developers through restructuring plans or reviewing Chinese technical documentation — Chinese lowers the comprehension barrier and conveys CJK typography and organization rules more precisely.

### 2.2 Why SKILL Files Instead of Agents?

`code-reader` outputs per-module `SKILL.md` files rather than creating dedicated module agents. The reasoning:

- **Decoupling & lightweight**: one agent per module would cause role proliferation and hard-code business logic into prompts. A `SKILL.md` extracts the "playbook" instead.
- **Load on demand**: any generic agent (e.g., a default coding assistant) can load a module's `SKILL.md` when needed and instantly "learn" that module's internals and modification rules.

---

## 3. Agent Skill Best Practices

From production-grade directory structure to progressive context loading, standardized engineering conventions are the foundation of stable agent skills. The practices below are adapted from [A "Standard Operating Manual" for Claude: Agent Skills in Practice and Deep Dive](https://github.com/ForceInjection/AI-fundamentals/blob/main/08_agentic_system/agent_skills/docs/claude_skills_guide.md) (Chinese).

### 3.1 Production-Grade Directory Structure

Separate core instructions, executable scripts, and reference material for maintainability:

- **`SKILL.md`**: the core operating manual; the filename MUST be uppercase.
- **`scripts/`**: executable scripts that perform atomic operations.
- **`references/`**: supplementary documents loaded on demand.
- **`assets/`**: static resources (images, templates).

### 3.2 Precise Trigger Descriptions

The `description` field in the `SKILL.md` frontmatter is the sole criterion a model uses to decide whether to load a skill. Follow the golden formula:

> **[Function] + [Trigger Scenario] + [Keywords]**

Be specific and scenario-driven; avoid vague or overly broad phrasing.

### 3.3 Progressive Disclosure

Three-layer progressive loading avoids context-window overflow when many skills are registered:

1. **Metadata layer (always loaded)**: skill names and descriptions only, forming a capability index.
2. **Core instruction layer (loaded on trigger)**: the full `SKILL.md` body is injected into context.
3. **Reference layer (loaded as needed)**: external documents under `references/`.

### 3.4 State Management & Workflow Orchestration

- **Not concurrency-safe**: unlike stateless function calls, Agent Skills dynamically mutate the current conversation context. Keep one skill active per conversation thread.
- **Complex workflows**: skills excel as "commanders" orchestrating workflows — multi-tool (MCP) collaboration, self-iterating correction, and context-based conditional branching.

### 3.5 Skill Testing Pyramid

Systematic testing keeps skills reliable as they evolve:

- **Trigger tests**: positive tests (skill triggers in target scenarios) and negative tests (no false triggers in unrelated conversations).
- **Functional tests**: verify the skill's underlying scripts or APIs return expected results.
- **Performance evaluation**: compare token consumption and interaction rounds with and without the skill.

### 3.6 Skill Naming Convention

Use the **noun/doer** form, not the verb (action) form: `agent-skill-reviewer` not `agent-skill-review`, `pdf-translator` not `translate-pdf`. Join multi-word names with kebab-case. This matches the skills' role as "personified" agent personas.

---

## 4. Deep Dive Case Studies

Beyond practical skills, this project contains deep-dive analyses of industry-leading AI engineering practices to help you build better virtual engineering teams.

### 4.1 gstack Deep Dive

A full reverse-engineering and architecture analysis of `gstack`, open-sourced by Y Combinator CEO Garry Tan, distilling its core design philosophy: **packaging structured software engineering roles as AI skills**. The report covers:

- **Headless browser daemon**: solving cold-start and state-loss issues when AI agents drive browsers.
- **Panorama of 21 core skills**: covering the full product lifecycle from planning to QA to release operations.
- **Prompt engineering best practices**: defensive design, cross-phase context inheritance, and expert mental models.

Read the full report: [gstack deep-dive](./docs/gstack-deep-dive-en.md)

### 4.2 Five Agent Skill Design Patterns

A translated and organized deep article from Google Cloud Tech on Agent Skill design patterns, helping you move beyond format and focus on the structured logic inside skills:

- **Tool Wrapper**: agents fetch specific library/framework context on demand.
- **Generator**: enforces consistent document output through templates and style guides.
- **Reviewer**: separates scoring criteria from the checking process for systematic multi-domain review.
- **Inversion**: the agent acts as an interviewer, blocking execution until full context is collected.
- **Pipeline**: enforces strict multi-step workflows through hard checkpoints.

Read the full report: [Five Agent Skill Design Patterns Every ADK Developer Should Master](./docs/google-skill-patern-en.md)

### 4.3 superpowers Deep Dive

A systematic engineering analysis and hands-on guide to the superpowers plugin and skill system: architecture layering, core modules, TDD/SDD workflows, subagent collaboration, and hook injection. Read the full report: [superpowers deep-dive](./docs/superpowers-deep-dive-en.md).

---

## 5. Recommended Resources

Beyond this project's built-in skills, the collections below — maintained by official vendors or the Force Injection blogger — demonstrate best practices in their respective domains.

| Repository | Domain | Summary |
|------------|--------|---------|
| [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills) | Full-stack dev & office docs | Official collection: frontend / fullstack / Android / iOS development, shader & GIF generation, PDF / PPTX / Excel / DOCX document processing |
| [ForceInjection/cuda-code-skill](https://github.com/ForceInjection/cuda-code-skill) | CUDA development | Official NVIDIA docs (PTX ISA, CUDA Runtime/Driver API, CUDA Math, cuBLAS, NCCL) converted to searchable Markdown, with GPU development skills for Claude Code / Trae |
| [vllm-project/vllm-skills](https://github.com/vllm-project/vllm-skills/tree/main) | vLLM deployment & benchmarks | Distributed as a Claude Code plugin; 6 skills: deployment (docker / k8s / simple) + performance benchmarks (serve / random-synthetic / prefix-cache-bench) |
| [ForceInjection/domain-driven-design-skills](https://github.com/ForceInjection/domain-driven-design-skills) | Domain-Driven Design | DDD strategic design, tactical design, and event-driven architecture (CQRS / Event Sourcing) packaged as agent skills |
| [franklinxkk/ai-delivery-spec](https://github.com/franklinxkk/ai-delivery-spec) | Requirements & SDD | Requirement management kernel for product managers: intake → clarify → PRD/contracts → review → baseline → change/acceptance evidence, with built-in CLI, domain packs, and structural gates |
| [ForceInjection/cufile-skill](https://github.com/ForceInjection/cufile-skill) | GPUDirect Storage | cuFile API lifecycle, sync / async / batch I/O, performance tuning, `cufile.json` configuration, and GDS compatibility checks (incl. `check_gds.sh`) |
| [ForceInjection/elf-skill](https://github.com/ForceInjection/elf-skill) | Binary security | elf-analyzer / binary-reverse / linux-pwn skill suite with built-in `allowed-tools` + `trust-level` security design |
| [ForceInjection/nvme-programming-skill](https://github.com/ForceInjection/nvme-programming-skill) | NVMe programming | Queue model & command construction, multi-queue tuning, NVMe 2.3 spec sections extracted as greppable text, 4 compilable C examples |

---

## 6. Skill Unit Testing

To prevent capability regression during iteration, this project builds a skill evaluation framework under `unit-test/`, based on automated execution scripts and behavior assertions:

- **Test runner**: `opencode-skill-eval.sh` automates end-to-end evaluation.
- **Guide**: [`skill-eval-minimal-guide-en.md`](./unit-test/skill-eval-minimal-guide-en.md) explains how to write and run skill evaluations.
- **Test cases & data**: `evals` (evaluation logic), `fixtures` (test data — e.g., sample documents for `doc-reviewer` and `md-translator`), `skills` (per-skill configs), and `tests` (assertion scripts).

Through systematic unit testing, we continuously validate trigger precision and execution reliability.
