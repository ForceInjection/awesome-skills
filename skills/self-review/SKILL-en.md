---
name: self-review
description: Pre-commit self-review of your own git diff — turns "confirm which repo/worktree holds the changes → read the full diff → run mechanical gates (coordinates + recorded results) → walk a six-class failure checklist → test on suspicion (including mutation self-checks) → grade verdicts into three tiers → declare that evidence matches the reviewed code" into a fixed checklist, and outputs verdicts of "fixed / pending / not-reproducible" with an audit trail. Use before committing your own changes (especially scripts, assertions/criteria, documentation numbers, and cross-repo reference surfaces), or when the user asks for a "git diff self-review", a "pre-commit check", or to "review my changes". Trigger words: self-review, diff review, pre-commit check, review my changes.
---

# self-review — Pre-commit Self-Review of Your Own git diff

**In one sentence**: before committing, read "what I just changed" as if it were **someone else's patch** — read the full diff first, then run the mechanical gates, then walk the failure-class checklist item by item, and finally grade the verdicts into three tiers (fixed / pending / not-reproducible). Reviewing is not "one more look"; it is **hunting for specific failure shapes from a checklist**.

## When to use

- Before a commit — especially when the changes touch **scripts, assertions/criteria, documentation numbers, or cross-repo reference surfaces** (these fail silently: no error, just quiet distortion)
- The user says "git diff self-review", "pre-commit check", or "review my changes"

## When not to use

- **Archived material is out of scope**: anything marked archive / frozen stays frozen — don't add consistency fixes to it, don't run its self-verification suite, don't write version records for it. When a real divergence is discovered, **state the fact in one sentence**; whether to attach a fix is the other side's call.
- Formal review of someone else's code → a formal code-review workflow (e.g. `/open-code-review`).
- Pure Markdown prose / typography → `/doc-reviewer`.
- **This diff only**: don't scope-creep into the whole repo, don't refactor untouched code.

## Workflow (six steps)

### 1. Establish coordinates

```bash
git status --short          # who changed what, who staged what — **don't touch other people's staged work**
git diff --stat             # scale
git diff --cached --stat    # staged surface
```

When changes come from multiple sources (me + the user / multiple sessions), first **list the paths that are mine** and hold every later step accountable to exactly that set; at commit time use `git commit -- <paths>` with path limiting so you don't swallow someone else's staged work.

**⚠️ First confirm "which repo/worktree holds the changes"** (verified 2026-09-29): when working across repos (a main repo plus several worktrees), running `git status` in repo A reads "clean" while all the changes live in worktree B — **that isn't clean, that's looking in the wrong place**. Technique:

```bash
git -C <tree> status --short          # run once per candidate tree; report HEAD too
git worktree list                     # include the other worktrees of the same repo
```

**Discipline: zero changes = a coordinates problem, not "all good"** — stop and switch trees instead of pressing on (`mech-gates.sh` now **exits 2** on this and lists other dirty worktrees, precisely so it can't be read as green).

### 2. Read the full diff (no sampling)

```bash
git diff -U2 -- <paths> > /tmp/rev.txt && wc -l /tmp/rev.txt
```

For a large diff, read it in slices (Read with offset/limit), **cluster by cluster**: scripts / criteria / docs / data. Sampling = skipping — and the skipped stretch is exactly where the problem lives (verified: a usage string missing a parameter and a stale counting convention both only surfaced on a full read).

### 3. Mechanical gates (let machines judge what machines can judge)

The script ships with this skill's directory; `<SKILL_DIR>` is the skill's install location:

```bash
bash <SKILL_DIR>/scripts/mech-gates.sh          # takes git diff --name-only HEAD + untracked
bash <SKILL_DIR>/scripts/mech-gates.sh <paths>  # specific files
```

It runs: `bash -n` (shell syntax), `ast.parse` (Python, **no pyc written**), conflict markers, trailing whitespace.

**Then add the gates the change surface itself carries** — provided the target is **still live**: the project's own unit tests / self-verification suite / parameter assertions / config parsing. After running, write the **command and result** into the verdict ("`bash -n` ×5 passed" is one sentence — don't paste full output).

**Record which code the gates ran on**: the script prints "repo under review + HEAD" first; for remote gates (ssh into a container/machine) add a line for the **tree / image / commit** — writing "ran it" alone is the same as writing nothing (nobody can later tell whether that evidence covers this diff).

**The reviewer's own evidence-gathering commands must pass C3 too**: `ssh … | tail` and `cmd | head` swap the **remote exit code for the pipe's** (`tail` is always 0) ⇒ remote failures silently pass. Use `set -o pipefail`, or read the critical output by hand (verified in practice: an e2e `PASS` was read out of the output, not given by the exit code).

### 4. Walk the failure-class checklist (this is the actual review)

The checklist lives in [`references/failure-classes-en.md`](references/failure-classes-en.md) — six classes: **criteria / failure direction / silent failure / consistent numbers / cross-repo cross-machine / commit surface**.

**Ask every class, one by one**: no requirement that each one hits, but **skipping is not allowed**. Rules are numbered `<class><index>` (A1…F6): the quick-scan table gives a one-liner, and the numbered details below it carry the full technique and instances; cite rules by number in verdicts (e.g. "see C3").

### 5. Suspicion means test it (discipline)

For any "I suspect there's a problem here" thought: **either immediately disprove/confirm it with a minimal experiment, or mark it "unverified"** — never let a hunch into the verdict and make the other side fix a problem that doesn't exist.

- Counter-example: suspecting that a newly added `prune` would judge the whole remote tree as leftover when the local list is empty, and `PRUNE_RM=1` would delete it all. Tested item by item (under `set -euo pipefail`, command-substitution failure ⇒ abort; `[ -f x ] && . x` is a set -e exempt form) ⇒ **not reproducible** — honestly recorded as "not reproducible" instead of "suggest adding a guard".
- The test must reproduce the **same shell**: same `set` combination, same redirection/pipe shape — a different shell invalidates the conclusion.

### 6. Evidence and reviewed code must be the same copy

**External evidence** cited in the verdict (real-machine runs / other people's logs / full container output) is only valid for **the copy of the code it ran on**. During self-review you often edit files (comments, stronger assertions, docs); after editing there are two compliant ways to close:

1. **Re-run** the gate (preferred, especially if the behavior surface changed); or
2. Explicitly declare the **difference surface** with supporting proof — "changes after that point are comments / tests / docs only, behavior surface untouched", evidenced by which files `git diff` touches and `grep -c <mutation-marker>` being 0 (proof a mutation test wasn't left behind).

Silently hanging old evidence on new code is not allowed. (Verified: after one self-review round touched 4 files, it took the declaration "changes after that point are comments/tests/docs only" plus `grep -c MUTATION-CHECK` = 0 to explain "e2e was not re-run yet the verdict still holds".)

## Verdicts in three tiers (no vague "worth watching")

| Tier                 | Meaning                                                               | Must include                                                                          |
| -------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Fixed**            | I changed it, and re-ran the mechanical gates after                   | `file:line` + one line of "before → after"                                            |
| **Pending**          | Needs the other side's call (convention / machine facts / trade-offs) | Facts + options + **my recommendation**                                               |
| **Not reproducible** | I suspected it, and testing disproved it                              | Test command and result (**keep the record**, so the same spot isn't suspected twice) |

**Keep the total to one glance**: one screen of table plus a few lines per tier. A review report is not a paper.

## After the review passes

**Run the mechanical gates once more before committing**: self-review itself edits files (the "fixed" items), so the gates must pass on the **final** copy of the code.

Three hard traps on the commit surface (details in failure-classes §F): path limiting carries exactly the listed paths, **renames must commit both halves**, and **the message goes to disk before the commit** (when retrying after a hook abort, reuse the same file verbatim — retyping tends to shrink it, and the short version lands in history). The commit action itself **requires authorization on the spot**; one authorization does not cover the next batch.
