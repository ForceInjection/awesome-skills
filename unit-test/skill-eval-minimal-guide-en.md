# Skill Testing: From "By Feel" to an "Evidence-Based" Quality System

This document explains how to complete "static unit tests" and "end-to-end evaluation" for Skills within the repository with minimal dependencies. Combined with systematic testing principles, our goal is to build a reproducible, comparable, CI-gatekept quality loop driven by deterministic signals (behavior and artifacts), compatible with any CLI-based open-source Code Agent (e.g., `OpenCode`), moving the team from "manual verification by feel" toward structured, reproducible, and comparable engineering governance.

---

## 1 Background and Goals

Skill creation has a low barrier to entry and the number of Skills is exploding, but the production of high-quality (stable, reusable, maintainable) Skills still lacks a systematic approach. Common problems include: unstable triggering (missed triggers / false triggers), deviation from steps, environment pollution (e.g., translation results polluting the codebase), and unenforceable style conventions.
Without metrics, it is difficult to tell whether a change is an improvement or a regression. Therefore, following the TDD principle of software engineering, we establish a testing loop for Skills: "evaluate only the results, not the path."

We generate reproducible metric signals through the following two layers:

- **Static layer (no LLM dependency)**: validates document assets and constraints (link formats, relative image paths, naming conventions, sensitive-information redaction), as a CI must-pass item.
- **Behavior layer (end-to-end sandbox)**: has the Agent actually execute the Skill, records the JSONL event stream, and asserts on tools, ordering, and key artifacts.

The evaluation focuses on the following **success dimensions**:

1. **Result**: whether the output is usable (whether reports are generated, whether formatting is preserved).
2. **Process**: whether the expected steps are followed (e.g., copy files to the sandbox first, then modify, to prevent main-branch pollution).
3. **Efficiency and consumption**: whether Token consumption stays within a reasonable range, and whether there is unnecessary "futzing around" (compared by parsing `usage.md`).

---

## 2 Directory and File Locations

The test framework achieves isolation and scheduling of multiple Skills through directory conventions; its core consists of a unified master script, per-Skill independent configuration sandboxes, and static rule sets.

- Code reference
  - Master script and entry point: `./unit-test/opencode-skill-eval.sh`
  - End-to-end executor: `./unit-test/evals/agent/run.sh`
  - Generic behavior assertor: `./unit-test/evals/agent/checks.js`
  - Usage and cost parser: `./unit-test/evals/agent/parse-usage.js`
  - Skill config and isolation environment: `./unit-test/skills/<skill>/config.sh`
  - Static unit test implementation and entry point:
    - Dispatch scheduler: `./unit-test/tests/run_static.py`
    - Rule-checking module: `./unit-test/tests/<skill>/checks.py`
  - Sample fixtures (test input samples): `./unit-test/fixtures/<skill>/input.md`

---

## 3 Static Unit Tests (Document Assets and Constraints)

Static tests do not depend on Agent or LLM reasoning. They use Python scripts to intercept format errors, dead links, and sensitive information up front, blocking low-level errors from flowing into the end-to-end stage and effectively reducing evaluation cost and noise.

- Scope of application
  - Link formats (only `http://` or `https://` allowed, with anchors `#` as an exception)
  - Relative image paths (absolute paths and `http(s)` external links prohibited)
  - File naming (lowercase + hyphens, no spaces or underscores)
  - Redaction of sensitive information (API Key/Secret, etc.)
- Run example

```bash
# Run the static unit test; it dispatches automatically by SKILL and outputs structured JSON (overall_pass/score/per-item booleans)
python3 ./unit-test/tests/run_static.py doc-reviewer
```

- Interpreting results
  - `overall_pass`: true when all checks pass
  - `score`: the ratio of passing items (0-1)
  - Per-item booleans: quickly locate the cause of failure (e.g., non-compliant naming)

---

## 4 End-to-End Evaluation (CLI Agents such as `OpenCode`)

End-to-end evaluation treats the Agent as a black box: it reconstructs the behavior trace by capturing the standard output of its CLI run (the JSONL event stream), then performs strict code-level assertions on tool call order, Token consumption, and the final generated artifacts.

### 4.1 Environment Preparation

The evaluation framework depends on global environment variables to inject the necessary API credentials and the basic Agent launch command.

```bash
# If the Agent needs an LLM provider, set it as needed, for example:
export OPENAI_API_KEY=your-key

# Set the CLI Agent command as an environment variable and enable JSON event output
export AGENT_CMD='opencode run --format json --print-logs'
```

### 4.2 Running and Generating the Trace

The master script routes execution by reading the `SKILL` environment variable: it launches the Agent, redirects standard output into a JSONL trace file, and automatically mounts the corresponding Skill's temporary sandbox workspace.

```bash
# Run the end-to-end evaluation; the Skill must be specified via an environment variable (e.g., doc-reviewer, md-translator)
# Note: do not pass the Skill name as a positional argument to the script, or a fool-proofing error will be triggered
SKILL=doc-reviewer bash ./unit-test/opencode-skill-eval.sh all

# Output files are located by default at:
# - Trace: ./unit-test/evals/artifacts/doc-reviewer.jsonl
# - Reports and artifacts: ./unit-test/evals/reports/doc-reviewer/
```

### 4.3 Behavior and Artifact Assertions

We codify the subjective judgment of "did it succeed" into Node.js scripts or Bash hook assertions. By parsing the `command_execution` and file-operation records in the JSONL trace, we can not only validate artifacts but also precisely detect whether the Agent has fallen into a retry loop ("futzing around"), and treat it as a CI red line.

```bash
# Parse the trace and assert key artifacts. The master script by default prioritizes the skill_after_artifact_checks hook in config.sh;
# if it is not defined, it falls back to the generic checks.js assertor.
SKILL=doc-reviewer node ./unit-test/evals/agent/checks.js \
  ./unit-test/evals/artifacts/doc-reviewer.jsonl \
  ./unit-test/evals/reports/doc-reviewer
```

- Interpreting results (example: `doc-reviewer`)
  - `hasOutline`/`hasContent`: whether each type of report was generated
  - `structureOk`: whether the report structure meets requirements
  - `score`/`overall_pass`: the deterministic behavior score and overall verdict

### 4.4 Run Results and Artifact Description

A single evaluation run generates an immutable behavior trace, sandbox-isolated temporary artifacts, and multi-dimensional resource-consumption reports. These deterministic physical files form the data foundation for troubleshooting and CI-automated gatekeeping.

- Event trace file (JSONL)
  - Path: `./evals/artifacts/${SKILL}.jsonl` (overridable by the Skill config)
  - Purpose: records the full event stream of `OpenCode` executing the Skill; appends `opencode stats` summary statistics at the end.
- Report and artifact isolation directory
  - Path: `./unit-test/evals/reports/${SKILL}` (overridable by the Skill config)
  - Purpose: automatically cleared before each run; stores the reports split out for the Skill, or serves as a "sandbox isolation zone" for temporary files (e.g., copied source documents), preventing the run from polluting the `fixtures` directory in the main codebase.
- Usage statistics report
  - Path: `./unit-test/evals/reports/${SKILL}/usage.md`
  - Purpose: extracts and aggregates the Token data used by the model (supports extracting the **Prompt Caching** and **reasoning/thinking Tokens** of modern LLMs) and the cost, assisting in evaluating stability and resource usage.
- Behavior assertion results (standard output)
  - Source: preferentially invokes the `skill_after_artifact_checks` hook in `config.sh` (customized per Skill); if not defined, falls back to the generic `node ./unit-test/evals/agent/checks.js`.
  - Form: prints key assertion fields as JSON

```json
# Note: sample output (fields may vary across Agent versions)
# You can collect this JSON directly into CI logs for gatekeeping decisions
{
  "hasOutline": true,
  "hasContent": true,
  "hasAssets": true,
  "hasFormat": true,
  "structureOk": true,
  "score": 1,
  "overall_pass": true
}
```

### 4.5 Run Modes and Parameters

The first positional argument of the master script (`MODE`) determines the injection strategy for the Agent's system prompt (Prompt), supporting a built-in full test and subset tests targeting specific functional modules.

- `content`: runs only the "content review", generating 1 report; the JSONL contains only events related to that review type.
- `all` (default): runs the four review types, generating 4 reports; the JSONL covers all event types; suitable for a complete end-to-end evaluation.
- Custom string: passed directly as a custom Prompt, adapting to personalized testing needs.

---

## 5 CI Recommendations and Threshold Gatekeeping

Combining static validation with behavior assertions in the pipeline builds an automated barrier that intercepts Skill capability regression. For models with non-deterministic output, we recommend introducing a `pass@k` multi-sampling strategy to balance pass rate and stability.

- **Strategy configuration**
  - Static layer: make `run_static.py`'s `overall_pass` a must-pass.
  - Behavior layer: make the `overall_pass` of `checks.js` (or the Skill-custom hook) a must-pass.
  - Advanced (pass@k): if the single-run success rate is below 100%, run multiple trials in CI (e.g., trials=5), compute pass@k (at least one success; measures capability) and pass^k (success every time; measures stability), and set thresholds based on business tolerance.
- **Troubleshooting**
  - Static failure: fix the document assets and constraints directly based on the Python script's error report.
  - Behavior failure: first inspect the command order, repeated executions, and error messages in the JSONL events to locate the root cause of the assertion failure.

---

## 6 How to Add Tests for a New Skill

To ensure framework extensibility, adding tests for a new Skill only requires following directory-based conventions and implementing config injection and assertion hooks - no changes to the master core script are needed.

- **Step 1: Prepare Test Data (Fixtures)**
  Prepare input samples (e.g., `input.md`) under `./unit-test/fixtures/<skill-name>/`. This is the source data the Agent works on; the framework automatically copies it into the sandbox directory at run time to prevent the original data from being polluted.
- **Step 2: Write Static Checks**
  Create static rules under `./unit-test/tests/<skill-name>/`. The master scheduler `run_static.py` automatically scans this directory and runs dependency-free quick validation (e.g., checking the Frontmatter completeness of `SKILL.md`).
- **Step 3: Create a Skill-Specific Config (`config.sh`)**
  Create `config.sh` under `./unit-test/skills/<skill-name>/`, using Bash hooks to override default behavior:
  - `build_target_doc`: defines the copy destination and sandbox path for the input document.
  - `build_prompt`: defines the test instructions injected into the Agent.
  - `skill_after_artifact_checks`: defines Skill-specific Node.js/Bash behavior assertions (checking whether files exist, whether formats are compliant, etc.).
- **Step 4: Run and Debug**
  Trigger an end-to-end run with `SKILL=<skill-name> bash ./unit-test/opencode-skill-eval.sh all`, and verify through `usage.md` and JSONL logs that Token consumption and retry behavior match expectations.

---
