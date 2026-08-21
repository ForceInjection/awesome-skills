# Deep Dive: mattpocock/skills — Packaging Engineering Discipline as Composable Agent Skills

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Design Philosophy: Composition Over Content](#2-design-philosophy-composition-over-content)
- [3. Core Patterns Deep Dive](#3-core-patterns-deep-dive)
  - [3.1 grilling: Design Trees and Frontier Rounds](#31-grilling-design-trees-and-frontier-rounds)
  - [3.2 wayfinder: Decision-Ticket Maps and Fog of War](#32-wayfinder-decision-ticket-maps-and-fog-of-war)
  - [3.3 tdd: Red-Green Governed by Seams](#33-tdd-red-green-governed-by-seams)
  - [3.4 diagnosing-bugs: The Loop Is the Skill](#34-diagnosing-bugs-the-loop-is-the-skill)
  - [3.5 writing-for-agents: A Self-Referential Meta-Skill](#35-writing-for-agents-a-self-referential-meta-skill)
  - [3.6 codebase-design: The Shared Vocabulary Foundation](#36-codebase-design-the-shared-vocabulary-foundation)
- [4. Skill Architecture: A Layered Composition System](#4-skill-architecture-a-layered-composition-system)
  - [4.1 User-Invoked vs Model-Invoked: A Principled Split](#41-user-invoked-vs-model-invoked-a-principled-split)
  - [4.2 CONTEXT.md: The Shared Vocabulary Layer](#42-contextmd-the-shared-vocabulary-layer)
  - [4.3 Process Gates and Completion Criteria: The Common Grammar](#43-process-gates-and-completion-criteria-the-common-grammar)
  - [4.4 Sub-Agent Dispatch: A Context Economy](#44-sub-agent-dispatch-a-context-economy)
- [5. Meta-Engineering: Managing the Repo as a Product](#5-meta-engineering-managing-the-repo-as-a-product)
  - [5.1 Dual-Track Distribution: Plugin Subscription vs Editable Copy](#51-dual-track-distribution-plugin-subscription-vs-editable-copy)
  - [5.2 Repo Governance: CLAUDE.md, ADRs, and Versioning](#52-repo-governance-claudemd-adrs-and-versioning)
- [6. Comparison with awesome-skills](#6-comparison-with-awesome-skills)
- [7. Takeaways](#7-takeaways)
- [8. Quick Start: 5 Minutes to First Use](#8-quick-start-5-minutes-to-first-use)

---

## 1. Project Overview

[mattpocock/skills](https://github.com/mattpocock/skills) is the personal agent-skill collection of Matt Pocock, the well-known TypeScript educator and founder of Total TypeScript. Open-sourced in 2026, it quickly became one of the most popular skill collections on GitHub (220k+ stars). The tagline says it all: "Skills for Real Engineers. Straight from my `.agents` directory." These are skills the author actually uses daily, not demo samples.

> **Reader's guide**: Chapters 1-5 explain the design (for everyone); chapter 6 is the comparison with this repo (author's perspective — casual users can skip it); chapter 7 gives actionable takeaways (each with a first step); chapter 8 is a 5-minute quick start. Want to try it directly? Start at chapter 8.

The repo ships 35 `SKILL.md` files organized into five buckets:

| Directory       | Purpose                                        |
| --------------- | ---------------------------------------------- |
| `engineering/`  | Daily code work (18 skills, promoted)          |
| `productivity/` | Non-code workflow tools (7 skills, promoted)   |
| `misc/`         | Kept around but not promoted (4 skills)        |
| `in-progress/`  | Public beta skills, feedback wanted (6 skills) |
| `deprecated/`   | Retired                                        |

The core philosophy is stated bluntly in the README:

> Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve. These skills are designed to be small, easy to adapt, and composable. They work with any model. They're based on decades of engineering experience.

Unlike process-owning frameworks (GSD, BMAD, Spec-Kit — methodology systems that try to take over the entire development process, e.g. GSD is GitHub's spec-driven workflow), the repo designs skills as **small, adaptable, composable units of discipline**: the author explicitly encourages users to "Hack around with them. Make them your own." It targets four real failure modes: **misalignment** (the agent didn't do what you wanted), **verbosity** (the agent uses 20 words where 1 will do), **broken code** (no feedback loops), and **ball-of-mud codebases** (accelerated software entropy).

---

## 2. Design Philosophy: Composition Over Content

If one word had to summarize this repo, it would be "composition". Unlike most repos where one skill = one complete manual, skills here form a pyramid:

- **Bottom layer**: model-invoked **primitive skills** — `grilling` (interviews), `domain-modeling`, `codebase-design` (deep modules), `tdd`, `research`, `prototype`, `code-review`, `diagnosing-bugs`. They carry all the methodology and can be triggered any time.
- **Top layer**: user-invoked **thin router skills** — `grill-with-docs`, `grill-me`, `wait-what`, `handoff`, `implement` (SKILL.md files are 7-16 lines). A router's body is often a single sentence; `grill-with-docs`'s entire SKILL.md is:

```markdown
---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Call the Skill tool twice, for "grilling" and "domain-modeling".
```

`grilling` is the most-reused primitive: five skills drive it (`grill-me`, `grill-with-docs`, `triage`, `wayfinder`, `improve-codebase-architecture`). `ask-matt` is the explicit map of the whole composition system — a "skill router" that answers "which skill fits my situation".

The payoff: methodology is written once, lives in one place (the primitive), and bug fixes are one-place edits; routers cost almost no context and only pull in primitives when the user actually needs them. The cost: composition relies on string conventions ("Call the Skill tool with X"), so when a user installs only a subset via skills.sh, router calls silently fail — an inherent risk of this architecture. The repo has no detection mechanism (the only install probe lives in `setup-matt-pocock-skills`), so new users should be aware.

`ask-matt` is more than a skill map: it encodes the repo's composition skeleton — the **"idea → ship" main flow** (`grill-with-docs` for alignment → `to-spec` to synthesize a spec → `to-tickets` to split into tickets → `implement` to build, driving `tdd` inside and closing with `code-review`), two on-ramps (`triage` and `diagnosing-bugs`), and the `prototype` → `handoff` detour bridge.

---

## 3. Core Patterns Deep Dive

### 3.1 grilling: Design Trees and Frontier Rounds

`grilling` is the repo's most popular pattern (the README calls `grill-me` / `grill-with-docs` "These are my most popular skills") and the answer to failure mode #1 (misalignment). It turns "let the agent ask the user questions" from casual conversation into structured discipline:

**Design tree**: every decision branches into the decisions that hang off it. The interview's goal is to traverse the whole tree until every branch is visited and nothing is silently assumed.

**Frontier rounds**: the whole frontier (every question whose prerequisites are already settled) is asked in one round. Each question is numbered and comes **with the model's recommended answer**, then the agent stops and waits for the user's answers before computing the next frontier. This batching is a subtle piece of attention economics — one wait buys answers to an entire patch of questions, instead of inefficient one-question-one-answer round trips.

**Division of labor**: _"Finding facts is your job, never the user's."_ When a frontier question needs facts from the environment, dispatch a sub-agent to find them without blocking the rest; but **decisions are always the user's** — put each one to them and wait.

**Termination**: the frontier is empty — every branch visited, nothing left silently assumed. Do not act until the user confirms shared understanding.

A `grilling` session looks like this (numbered questions with recommended answers, the whole frontier asked in one round):

```
❓ **Q1** - **Scope**: Which features does this change cover, and what is explicitly out?

➡️ I'd suggest starting with the core flow only, deferring edge cases to phase two

❓ **Q2** - **Data model**: Does the current schema need migration?

➡️ I'd suggest not — additive fields should suffice
```

(The ADRs mentioned in grill-with-docs's description are Architecture Decision Records — short documents recording "why this design", so future maintainers without context don't mischange it.)

### 3.2 wayfinder: Decision-Ticket Maps and Fog of War

### 3.2 wayfinder: Decision-Ticket Maps and Fog of War

`wayfinder` is one of the most serious structured answers to "large work that won't fit in one agent session". Core insight: **planning across sessions must be a shared artifact, not session state**.

- **Destination**: the map's anchor. Naming it is the first act of charting and shapes every ticket — it might be a spec to hand off, a decision to lock, or a change made in place.
- **Decision tickets vs execution tickets**: tickets on the map are **decision tickets** — they resolve a decision, not a slice of a build to execute. Wayfinder is _planning_ by default ("plan, don't do"): the map is done when the way is clear, not when deliverables land.
- **Fog of war**: the map is deliberately incomplete. Decisions you can tell are coming but can't pin down yet live in the fog, recorded in the map's **Not yet specified** section. The test is "can you state the question precisely now", not "can you answer it now". Fog only ever gathers _toward_ the destination; work consciously ruled out goes to **Out of scope**, which never graduates.
- **Native blocking**: dependencies use the tracker's native blocking relationship, so the frontier renders visually in the tracker's UI — the human sees what's takeable without opening the map.
- **Claim-by-assignment**: a session **assigns itself as the ticket's assignee first**, before any work, so concurrent sessions skip it — concurrency is a first-class citizen.
- **Hard rule**: _"Never resolve more than one ticket per session"_ (except research tickets). Each ticket is sized to a 100K-token agent session.
- **Four ticket types**: Research (AFK — the agent reads alone), Prototype (HITL — a cheap concrete artifact to react to), Grilling (HITL — conversation, the default), Task (HITL or AFK — manual work that must precede a decision, e.g. signing up for a service, migrating data). HITL = human-in-the-loop; AFK = away-from-keyboard (agent-driven alone). The type decides who resolves a ticket and how.

### 3.3 tdd: Red-Green Governed by Seams

`tdd` reframes the red→green loop as **seam governance**. Its goal isn't to teach the agent to run TDD; it's to make the loop "produce tests worth keeping":

- **Tests live only at pre-agreed seams**: a seam is the public boundary where you can observe behavior without reaching inside — tests live there, never against internals. Before writing any test, write down the seams under test and confirm them with the user — _"No test is written at an unconfirmed seam."_ You can't test everything, so pre-agreeing seams is how testing effort lands on critical paths and complex logic instead of every edge case.
- **Three anti-patterns**, each with its tell:
  - **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel. Tell: the test breaks on refactor while behavior is unchanged.
  - **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`). Expected values must come from an independent source of truth.
  - **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior — you test the shape of things rather than user-facing behavior. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** responding to what the last cycle taught you.
- **Refactoring is not part of the loop**: it belongs to the `code-review` stage, keeping the red→green cycle undiluted.
- **Cross-skill composition**: when the interface shape itself is in question (how deep the module is, where the seam belongs), call `codebase-design` for the vocabulary — "a reference to consult, not a session to run".

### 3.4 diagnosing-bugs: The Loop Is the Skill

`diagnosing-bugs`'s manifesto: **"Phase 1: Build a feedback loop. This is the skill. Everything else is mechanical."**

- **Loop before hypothesis**: _"No red-capable command, no Phase 2."_ (No command that can go red on this bug, no Phase 2.) If you catch yourself reading code to build a theory before this command exists, stop: "jumping straight to a hypothesis is the exact failure this skill prevents."
- **Ten ways to construct a loop**, in priority order:
  1. Failing test at whatever seam reaches the bug (unit, integration, e2e)
  2. Curl/HTTP script against a running dev server
  3. CLI invocation with a fixture input, diffing against a known-good snapshot
  4. Headless browser script (Playwright/Puppeteer) driving the UI and asserting on DOM/console/network
  5. Replay a captured trace (save a real request/payload/event log, replay it through the code path in isolation)
  6. Throwaway harness (a minimal subset of the system with mocked deps, one function call exercising the bug path)
  7. Property/fuzz loop (for "sometimes wrong output" bugs: 1000 random inputs, look for the failure mode)
  8. Bisection harness (bug appeared between two known states: automate "boot at state X, check, repeat" for `git bisect run`)
  9. Differential loop (same input through old vs new version, diff outputs)
  10. **HITL bash script** (last resort — human-in-the-loop: when a human must click, drive them with a template so the loop stays structured; captured output feeds back to you)
- **Completion criterion is a checkable checklist**: Red-capable (drives the actual bug path and asserts the user's exact symptom) / Deterministic / Fast (seconds) / Agent-runnable (unattended).
- **Tighten the loop**: treat it as a product — faster? sharper signal? more deterministic? "A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight, a debugging superpower."
- **Non-deterministic bugs**: the goal is not a clean repro but a **higher reproduction rate** — loop 100×, parallelize, add stress, inject sleeps. "A 50%-flake bug is debuggable; 1% is not."
- **Hypotheses must be falsifiable**, stated in a fixed format: "If <X> is the cause, then <changing Y> will make the bug disappear." A predictionless hypothesis is a vibe: discard or sharpen it. Show the ranked list **to the user before testing** — they often re-rank it with one sentence.
- **Redaction discipline**: redact every secret first; tag debug logs with a unique prefix (`[DEBUG-a4f2]`) so cleanup is a single grep.
- **"No correct seam is itself the finding"**: if the only available regression-test seam is too shallow, that's a discovery — the codebase architecture is preventing the bug from being locked down. Flag it and bridge to `improve-codebase-architecture`.

### 3.5 writing-for-agents: A Self-Referential Meta-Skill

`writing-for-agents` is "the document about how to write documents for agents" — the quality source behind every SKILL.md in the repo, and one of the few public attempts to theorize skill writing. Its toolbox:

- **Context pointers**: a reference held in context that names out-of-context material and encodes the condition for reaching it. A skill's description is one; a line in `AGENTS.md` is the same object. **The pointer's wording, not its target, decides when and how reliably the agent reaches the material.** "A must-have target behind a weakly worded pointer is a variance bug" (the same input producing inconsistent outputs across runs): sharpen the wording first, inline only if sharpening fails.
- **The two loads**: Context load (the token cost of always-loaded material) vs Cognitive load (the human's burden — the human is the index). A pointer escapes context load at the price of its own line; material with no pointer rides entirely on cognitive load.
- **Information hierarchy ladder**: in-file step (the primary tier, ordered actions) → in-file reference (definitions consulted on demand) → disclosed reference (pushed to a separate file, reached by a pointer). Progressive disclosure is the move _down_ the ladder; branching is the cleanest disclosure test — inline what every branch needs, disclose what only some branches reach.
- **Leading words**: compact concepts already living in the model's pretraining (_tight_, _red_, _fog of war_, _tracer bullets_), repeated as tokens — never sentences — to recruit priors. "fast, deterministic, low-overhead" → _tight_; "a loop you believe in" → _red_ (a fuzzy gate becomes a binary observable state). Coining your own word costs definition tokens; reach for an existing word first.
- **Negation is the failure mode**: "don't think of an elephant", and the elephant is all there is — the ban drags the forbidden behavior into context and makes it _more_ available. State the positive target; a prohibition earns its place only as a hard guardrail you cannot phrase positively, and even then, pair it with the positive target.
- **Completion criteria**: Clarity (can the agent tell done from not-done — a vague bound invites premature completion) and Demand ("every modified model accounted for" forces thorough work).
- **Pruning discipline**: single source of truth (no duplication); the environment is a source of truth too (`package.json`, `--help` — restating it makes a document a cache); relevance checks (against sediment — "the default fate when adding feels safe and removing feels risky"); the **no-op test** ("does this line change behavior versus the default? If not, delete the whole sentence, not words").

### 3.6 codebase-design: The Shared Vocabulary Foundation

`codebase-design` is the repo's **shared vocabulary base**, packaging Ousterhout's deep-module philosophy ("the best modules are deep: a lot of functionality behind a small interface") as mandatory terminology: module / interface / depth / seam / adapter / leverage / locality. It is referenced by `tdd` and `improve-codebase-architecture`.

Notable writing techniques:

- **Mandatory glossary**: "Use these terms exactly... Consistent language is the whole point." With an `_Avoid_` list.
- **Principles stated as tests**: the deletion test (a complexity-conservation check — imagine deleting the module: if the complexity vanishes it was a pass-through; if it reappears across N callers, it was earning its keep), "one adapter = hypothetical seam, two = real".
- **Rejected framings section**: actively records definitions that were rejected — preventing the model from falling back to folk wisdom like line-count ratios.
- **DESIGN-IT-TWICE.md**: a **parallel design contest** — 3+ sub-agents each given a different bias constraint (minimal interface / maximal flexibility / common-caller-first / ports-and-adapters) design independently, then compare on depth / locality / seam and give a decisive recommendation. One of the most creative uses of sub-agent dispatch.

---

## 4. Skill Architecture: A Layered Composition System

### 4.1 User-Invoked vs Model-Invoked: A Principled Split

Every skill chooses one of two invocation modes:

- **User-invoked**: `disable-model-invocation: true` (OpenAI ecosystem: `policy.allow_implicit_invocation: false`); reachable only when the human types a slash command. Their job is **orchestration** — carrying stateful session flows.
- **Model-invoked**: reachable by the model or the user; they hold the reusable discipline — the agent reaches for them automatically when the task fits.

The criterion is self-documented in `writing-for-agents/SKILL-MECHANICS.md`: user-invoked skills cost zero context but need a human trigger; model-invoked skills carry their trigger branches in their description wording. The README sums it up: "User-invoked skills orchestrate; model-invoked skills hold the reusable discipline. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one."

### 4.2 CONTEXT.md: The Shared Vocabulary Layer

`CONTEXT.md` is the single source of truth for a project's shared language — a **pure glossary**, "totally devoid of implementation details"; not a spec, not a scratchpad. It defines domain terms (Issue tracker / Issue / Decision ticket / Triage role), each with an `_Avoid_` list, plus a "Flagged ambiguities" section recording terms that were once ambiguous and are now resolved.

Several engineering skills (e.g. `tdd`, `diagnosing-bugs`) open with the same instruction: "read `CONTEXT.md` (if it exists)... respect ADRs in the area you're touching." Vocabulary is the glue of cross-skill composition: `tdd` uses `codebase-design`'s seam vocabulary, and `code-review`'s Spec axis (see 4.4) checks the spec. The `domain-modeling` skill actively builds and sharpens this glossary, with an ADR three-condition gate (hard to reverse + surprising without context + real trade-off — only then write an ADR).

Notably, **the repo applies its own methodology at the meta level**: its own CONTEXT.md is the product of this glossary system, `.out-of-scope/` records rejected requests to prevent repeat suggestions, and ADRs document real trade-offs like "why ship a Claude Code plugin rather than a Codex one".

### 4.3 Process Gates and Completion Criteria: The Common Grammar

Almost every skill uses the same grammar: **explicit process gates + checkable completion criteria**.

- "No red-capable command, no Phase 2." (diagnosing-bugs)
- "Never resolve more than one ticket per session." (wayfinder)
- "Do NOT interview the user." (to-spec — synthesizing discussed content into a spec forbids re-interviewing)
- "No test is written at an unconfirmed seam." (tdd)
- "Always resolve; never --abort." (resolving-merge-conflicts — resolve by intent, trace each side's primary source, never abandon the merge)
- Completion criteria as checklists (diagnosing-bugs's four checkboxes, wizard's "Done when…")

This is the direct product of `writing-for-agents`'s completion-criteria theory (Clarity + Demand) — the repo practices what it teaches.

### 4.4 Sub-Agent Dispatch: A Context Economy

Sub-agent dispatch is standard operating procedure, with a clear economic view of "what belongs in a sub-agent window":

- **code-review**: two axes (Standards / Spec) run as parallel sub-agents so neither pollutes the other's context — this is the reranking phenomenon isolation is designed to prevent.
- **grilling**: facts needed by frontier questions go to sub-agents without blocking the rest.
- **research**: the whole skill is "delegating the reading legs to a background agent, trusting only primary sources, producing a cited Markdown file".
- **wayfinder**: research tickets fan out to parallel sub-agents.
- **improve-codebase-architecture**: codebase exploration goes to sub-agents.
- **DESIGN-IT-TWICE**: a parallel design contest.

The other half of the context economy is **session hygiene**, defined in `ask-matt/PHASE-BOUNDARIES.md`: a five-option decision tree (Continue / `/clear` / `/handoff` / Subagent / `/compact`) ordered by the economics of primary vs secondary sources — Continue is ruled out first, `/clear` is cheapest, `/handoff` only for a harness change, directory change, person change, or mid-effort fork, and `/compact` is last resort. Paired with the **smart zone** (~150k tokens — the window within which the model still reasons sharply): `ask-matt` recommends keeping one uninterrupted window from grilling to `to-tickets`, and handing off or compacting past it.

---

## 5. Meta-Engineering: Managing the Repo as a Product

### 5.1 Dual-Track Distribution: Plugin Subscription vs Editable Copy

Two install paths, two philosophies:

- **Claude Code plugin** (`.claude-plugin/`): `claude plugins install mattpocock-skills`, a managed, read-only, auto-updating bundle in the official marketplace — **subscribe rather than fork**. The plugin ships exactly the 25 promoted skills from `engineering/` and `productivity/`; misc / in-progress / deprecated never appear.
- **skills.sh** (`npx skills add mattpocock/skills`): copies skill files into your project as ordinary files you own and edit — "Nothing updates behind your back". Works for Codex and any Agent-Skills-standard harness.

An onboarding skill accompanies both: `/setup-matt-pocock-skills` runs once per repo, asking which issue tracker (GitHub / Linear / local files), triage label conventions, and where to save docs. Engineering skills get the tracker abstraction through per-tracker config files generated by setup (`issue-tracker-github.md` / `issue-tracker-gitlab.md` / `issue-tracker-local.md`, one per tracker), with the uniform phrasing "should have been provided to you; run `/setup-matt-pocock-skills` if not".

**How to choose**: want zero maintenance and to follow the author's updates — pick the plugin subscription. Want to adapt the skills to your own workflow, or use non-Claude harnesses like Codex — pick skills.sh. And note the README warning: **don't install both** — "installing both leaves you with every skill twice".

### 5.2 Repo Governance: CLAUDE.md, ADRs, and Versioning

The governance density is rare among skill repos:

- **CLAUDE.md / AGENTS.md** are complete operating manuals for AI maintainers: bucket conventions, plugin.json sync rules, docs-page mirror rules, the rule that `ask-matt`'s router map must stay accurate ("a router that lies" is an explicit failure mode), and `scripts/link-skills.sh` symlink distribution.
- **ADRs** (`.agents/adr/`): real architecture decisions — `0002-ship-as-a-claude-code-plugin.md` analyzes in depth why to ship a Claude Code plugin but not (yet) a Codex one (Codex manifests accept only a single path; symlinks don't survive install), and why the setup pointer belongs only in hard-dependency skills (soft-dependency skills stay token-light, no cargo-culting).
- **Versioning**: `.changeset/` manages every skill tweak (even "add separators between grilling questions" gets a changeset); `sync-plugin-version.mjs` keeps plugin and package versions in lockstep.
- **Docs mirror**: every promoted skill has a human-readable page at `docs/<bucket>/<skill>.md` with a uniform four-section structure: What it does / When to reach for it / Common questions / It's working if.
- **Style rule**: no em-dashes anywhere in the repo's prose — rewrite with commas, colons, parentheses, or conjunctions.

## 6. Comparison with awesome-skills

| Dimension         | awesome-skills (this repo)                                                        | mattpocock/skills                                                                                          |
| ----------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Skill shape       | Large self-contained SKILL packages (30-224 lines each)                           | Small composition: primitives + thin routers (7-140 lines; methodology written once)                       |
| Composition       | Skills mostly independent, triggered by description                               | Routers explicitly call primitives ("Call the Skill tool twice"); `ask-matt` is the explicit map           |
| Shared vocabulary | No repo-level glossary; the bilingual (EN/CN layered) convention is the main norm | CONTEXT.md as single source of truth + ADRs, read by nearly every skill                                    |
| Invocation split  | Not distinguished                                                                 | `disable-model-invocation` principled split, self-documented criterion                                     |
| Testing           | unit-test/ testing pyramid (static + end-to-end JSONL assertions)                 | Almost no testing system (confirmed weakness)                                                              |
| Distribution      | `sync.sh` copies to three local harnesses                                         | Claude Code official marketplace + skills.sh, changeset versioning                                         |
| Deep dives        | Three deep-dive articles (gstack / google / superpowers)                          | None (practice-first)                                                                                      |
| Unique assets     | Bilingual docs system, testing pyramid, four-type review (doc-reviewer)           | grilling design trees, wayfinder decision-ticket maps, writing-for-agents, diagnosing-bugs loop discipline |

Overlap: our `openspec-assistant` (spec-driven development) and their `to-spec → to-tickets → implement → tdd → code-review` pipeline are both SDD, but complementary — ours emphasizes role collaboration (Architect / Developer / QA) with the `/opsx` command system; theirs emphasizes disciplined small-step pipelines. Our `doc-reviewer`'s four review types and their `code-review`'s two axes (Standards + Spec) are also worth cross-referencing.

## 7. Takeaways

Each takeaway comes with a **first step** — actionable as soon as you finish reading; the mechanics live in the referenced section.

1. **Composable skill architecture is worth experimenting with** (see §2): converging methodology into a few primitives (grilling, domain-modeling, codebase-design) with thin user-facing routers makes fixes and evolution one-place edits. The cost is needing a router map like `ask-matt` to prevent "too many skills, can't find the one".
   - **First step**: pick one of your thick skills and extract one reusable flow (e.g. "ask before acting") into a standalone primitive, then turn the main skill into a one-line router calling it — a single experiment, no full refactor.
2. **The CONTEXT.md vocabulary layer is the most underrated design** (see §4.2): several skills read the same glossary, keeping terms, variables, and filenames consistent while cutting agent navigation cost and token usage. `grill-with-docs` binds alignment interviews to vocabulary sedimentation — one session produces both a shared language and ADRs: "it might be the single coolest technique in this repo".
   - **First step**: write a 20-line glossary for your current project (10 domain terms, each with an `_Avoid_` list), put it in `CONTEXT.md`, and add one line to your skill: "read CONTEXT.md before acting".
3. **Process gates beat verbose instructions** (see §4.3): explicit gates like "No red-capable command, no Phase 2" turn discipline into hard constraints; paired with checkable completion criteria, they outperform "please be sure to establish a feedback loop first" by a wide margin.
   - **First step**: open one of your SKILL.md files, find the vaguest "please/be sure to" instruction, and rewrite it as a gate ("no X, no next phase") plus a completion criterion.
4. **When writing skills, be aware that negation is a failure mode** (see §3.5): state the positive target behavior; use prohibitions only as hard guardrails that cannot be phrased positively, and always pair them with the positive target. This single rule can improve the writing of all our SKILL.md files.
   - **First step**: grep your skill directories for "don't/never/avoid", rewrite each as a positive statement. Example — original: "don't modify the user-provided title"; rewritten: "keep the user-provided title as the main title verbatim; put distillation and summary in the subtitle". (This example is adapted from an existing rule in our own `editorial-card-designer`.)
5. **Meta-engineering bootstraps itself** (see §4.2, §5.2): managing your own repo with the discipline you teach (CONTEXT.md managing its own vocabulary, ADRs recording its own architecture decisions, `.out-of-scope/` preventing repeat suggestions) means every methodology has passed the test of real use.
   - **First step**: write a `CONTEXT.md` for your repo (even 5 terms), and write one ADR the next time you make a hard-to-reverse decision — start with these two, add the rest as needed.
6. **Pay the price of composition up front** (see §2): heavy reliance on the author's personal conventions (CONTEXT.md / triage labels / the smart-zone assumption of ~150k tokens of sharp reasoning) raises the cognitive load on new users; cross-skill composition has no fallback, so routers silently break when a subset is installed.
   - **First step**: if you only want 2-3 skills, install them selectively via skills.sh and manually verify that the cross-skill calls those skills make are present (see §5.1).
7. **Skill quality needs test assurance**: the repo's near-total absence of a testing system is its biggest weakness — which backfires as confirmation that "skill quality needs test assurance" is the right call, and is exactly where our unit-test pyramid (static + end-to-end JSONL assertions) provides value.
   - **First step**: no external action needed — it endorses our existing test investment; keep adding tests for new skills via `unit-test/`.

## 8. Quick Start: 5 Minutes to First Use

You don't need to read the whole article to try this repo:

1. **Install the plugin** (Claude Code users, 30 seconds):
   ```bash
   claude plugins install mattpocock-skills
   ```
   Or get an editable copy (works with Codex and any harness):
   ```bash
   npx skills add mattpocock/skills
   ```
   **Pick one path — don't install both** (you'd get every skill twice).
2. **Run the setup wizard once per repo**: `/setup-matt-pocock-skills` — answer three questions (issue tracker, triage labels, docs directory). Skippable if you only use the productivity skills.
3. **5-minute experiment**: run `/grill-me` on a vague idea you have (a feature, a refactor, an article) and experience the design-tree/frontier interview (§3.1). This is the author's signature skill.
4. **Skills worth trying first**, by scenario:
   - Writing code with a team: `/grill-with-docs` (alignment + vocabulary), `/tdd` (seam governance)
   - Planning large work: `/wayfinder` (decision-ticket maps, §3.2)
   - Debugging a nasty bug: `/diagnosing-bugs` (loop discipline, §3.4)
   - Want to see how its skills are written: read `skills/productivity/writing-for-agents/SKILL.md` — the quality source for every skill in the repo (§3.5)
5. **Not sure which to use**: ask `/ask-matt` — it routes you through the main flow (§2).
