# Failure-Class Checklist (execution surface for self-review step 4)

Six classes, rules numbered `<class><index>` (A1…F6). Each class opens with a **quick-scan table** (one line per rule); the numbered **details** below the table carry the full technique and instances. Cite rules by number (e.g. "see C3", "add a mutation per A2").
Ask every class in order; whatever hits goes into the verdict (fixed / pending / not-reproducible).

## A. Criteria class — the most expensive class: wrong criteria make all-green meaningless

| #   | Symptom                                            | Quick check                             |
| --- | -------------------------------------------------- | --------------------------------------- |
| A1  | Criteria and judged object misaligned              | Align against production call-site args |
| A2  | Tautological criteria (no discriminative power)    | Known positives/negatives + mutation    |
| A3  | Grouping coupled to wall clock or implementation   | Clock-independent keys; negative run    |
| A4  | Threshold changed, criteria set has no version row | Threshold change ⇒ check version table  |
| A5  | Missing data / not-applicable / fail conflated     | Three states separable and observable   |
| A6  | Stub and production contract disagree              | Compare guards and failure paths        |
| A7  | Instrumentation fields always zero                 | Ask where the accumulation point is     |
| A8  | Diagnostic code's type contract wrong              | Per value, ask the production type      |

**A1 Criteria and judged object misaligned** (shape / unit / index domain)
Align the criteria's input shape against **the production call sites' actual arguments** one by one (`grep` the call sites); ask "what domain is my index in, and what domain does the other side index by".
Example: a guard function wanted **node objects** while production passed **id lists** ⇒ `getattr` always empty ⇒ guard structurally dead, while unit tests fed it objects ⇒ a whole field of green.

**A2 Tautological criteria** (no discriminative power)
Run a **known negative**: undetected = always green; then a **known positive**: error raised = false positive. Both must pass before the criterion stands. **Newly written / strengthened assertions get a minimal mutation on top**: remove the protection being tested (rollback / validation / guard), and the assertion **must turn red** — still green under mutation = no discriminative power.
Example: `grep -c '<pat>' == 0` judged PASS — with a typo'd pattern it's always green; `-qF` substring matching let a **similar unrelated word** pass too. Mutation case: a "rollback must error" assertion originally checked only the **first** failure item ⇒ always green even without rollback; after rewriting it as "request ≈ full capacity first, then over-capacity", removing the release call under test turned it red immediately.

**A3 Grouping/numbers coupled to wall clock or implementation details**
Grouping keys must be clock-independent (**step-aligned**); validate discriminative power on a known-negative run first.
Example: grouping **by second** ⇒ one step landing across a second boundary read as split (false positive); grouping by `(rids,n)` ⇒ real divergences split apart and missed (false negative).

**A4 Threshold/convention changed but the criteria set has no version record**
Thresholds are part of the criteria ⇒ change a threshold, then check the version table got a row.
Example: without recording the landing-rate threshold 0.20, "runs before this row can't be read alongside runs after it" becomes impossible.

**A5 Missing data / not-applicable / judged-fail conflated**
The three must be **separable and observable** (each with its own reading bit); with a two-state verdict, the reason field says "missing data" — don't invent a third state.
Example: writing "no evidence collected" as "pass"; a real-machine arm carrying an unerasable "not applicable" ❌ every run.

**A6 Stub and production contract disagree** (stub missing the production guard / idempotency / one-shot / failure branch)
Compare one by one against the **guards and failure paths** of the replaced object: early `return`, idempotency latch, one-shot, `except` branch — production has it and the stub doesn't = that bug class **doesn't exist** in unit tests.
Example: a registration entry point's first line `if self._ready: return` (one-shot) was missing from the stub ⇒ the whole bug class "late registration silently swallowed" stayed green in tests and only 500'd on real hardware. **Fix = stub replicates the guard**, plus a test case "late registration must be judged False".

**A7 Instrumentation fields always zero** (fake readings read as "no overhead")
For every timing/counter field, before it ships ask "where is its **accumulation point**"; new instrumentation ships with a "fields all present" regression test (rename / dropped field / NameError turns red on the spot). **When a field gets read into a conclusion it's worse** — prefer deleting an always-zero field.
Example: three timing fields initialized and never accumulated, printing 0.0 forever ⇒ wrongly judged "non-DMA overhead negligible"; the truth hid outside the timing window (ref/unref totaling 17-46 ms, surfaced only by a supplementary measurement).

**A8 Diagnostic code's type contract wrong** (probe reads a value whose type ≠ the production type) — same family as A1, but the consequence is the **probe crashing the host process itself**
For every new probe, per value ask "**what type is it in production**": a `torch.Tensor` **must not** go through `x or []` / `if x` (`bool(tensor)` on a multi-element tensor raises `RuntimeError` directly); use `.numel()`; sequences use `len()`. Wrap the probe body **entirely in try/except with degradations recorded** (a probe may degrade, never take the host down). Regression tests **feed production-shaped arguments** (tensor in, tensor) + mutation self-check (revert the probe to the old shape ⇒ must turn red).
Example: a boundary probe wrote `len(getattr(item,"device_value",[]) or [])` while the value was a tensor ⇒ 30 s after startup, the first warmup step boundary fired `RuntimeError: Boolean value of Tensor…` ⇒ four ranks SIGQUIT at the same instant, the container reaped by the launch script on timeout (**a long run never once completed**).

## B. Failure-direction class — destructive/overwriting actions must be conservative

| #   | Symptom                                  | Quick check                        |
| --- | ---------------------------------------- | ---------------------------------- |
| B1  | Incomplete guards on destructive actions | List failure paths, ask each       |
| B2  | Fail-open: no verdict, let it through    | Ask "where does the path lead"     |
| B3  | Silent degradation                       | Check soft fallbacks leave a trace |

**B1 Incomplete guards on destructive actions**
List the failure paths one by one (empty input / target missing / command failed / pipe swallowing codes), ask "what happens on each".
Example: three guards before deleting remote files: target in place, delete list non-empty, **delete count ≠ full set** (the last means a distorted baseline — refuse to delete).

**B2 Fail-open**: can't get a verdict, so let it through
Ask "where does this un-judgeable path lead"; cross-replica consistency criteria must fail closed.
Example: voting couldn't get a verdict ⇒ let it through ⇒ each rank judged for itself ⇒ batch shapes diverged ⇒ hang.

**B3 Silent degradation**: on error, fall back to a default and keep running
Check each `except: pass` / `return None` / `|| true` for **whether it leaves a trace** — a soft fallback shaped like "nothing was wrong" is the same as having no criterion.
Example: allocation failure did `rollback + return None` without logging a line; causality could only be inferred backwards from "the line that should appear, doesn't".

## C. Silent-failure class — "the command looked successful, but nothing landed"

| #   | Symptom                                     | Quick check                             |
| --- | ------------------------------------------- | --------------------------------------- |
| C1  | Hardcoded defaults                          | Coordinates read one source, else error |
| C2  | Truncation / rate limits swallow evidence   | Ask if the swallowed part was the point |
| C3  | Substitution / pipes / assignment eat codes | Check set -e / pipefail; own tools too  |
| C4  | Arguments never reached the container       | Assert once set; don't pass defaults    |

**C1 Hardcoded defaults** downgrade "ran wrong" into "silent"
Coordinate-type values (paths / hosts / image tags / tree names) must read from a **single source** and **error out** when missing, not fall back to a literal.
Example: two scripts each hardcoded a default tree ⇒ they landed on **different trees**, synced another line's code while health still returned 200.

**C2 Truncation / rate limits swallow evidence**
Seeing `| head -N` or "first N + every M", ask: could the swallowed part be exactly what needed reading.
Example: a set difference `| head -10` ⇒ of 21 leftovers only 10 showed per run; three rm rounds to finish.

**C3 Command substitution / pipes / assignments swallow exit codes**
Is the return value of `$(...)` checked; does the script have `set -e`; do **pipes** have `set -o pipefail`. **The reviewer's own evidence-gathering commands count too** — `ssh … | tail` returns `tail`'s exit code.
Example: a remote `cd` failed ⇒ empty output ⇒ locally judged "no leftovers"; `ssh host '… | tail -8'` let a remote failure pass silently (verified in practice: e2e pass/fail was decided by a human reading `PASS`, the exit code never counted).

**C4 Arguments never reached the container / set but ineffective**
Once set, **assert it** (`docker exec env | grep -qx`); don't pass defaults explicitly (passing them means you can no longer prove "not passing is also right").
Example: a missed `-e` item ⇒ the tree self-check never ran all session, heartbeats all 0, invisible in the logs.

## D. Consistent-numbers class — docs vs implementation

| #   | Symptom                                | Quick check                                 |
| --- | -------------------------------------- | ------------------------------------------- |
| D1  | Counts / tallies / thresholds differ   | Count any documented number on the spot     |
| D2  | References not updated after rename    | Repo-wide grep for the old name             |
| D3  | Dangling references                    | Search after move/delete; point to new spot |
| D4  | Verdict contradicts the implementation | Reason says "missing data", no 3rd state    |
| D5  | Motivation sentences rot               | Grep numbers and "whys" vs latest data      |
| D6  | Disproved evidence left in docs        | Field-check excerpts; replace with pointer  |

**D1 Counts / tallies / thresholds differ between the two sides**
Any number written in docs gets **counted on the spot** (`grep -c` / script self-report).
Example: docs said "22 items = 5 + 17", actual count 24; elsewhere in the same batch the number had already been de-hardcoded.

**D2 References not updated after a rename** (paths / branch names / image tags)
After renaming, repo-wide `grep -rn <old-name>`: confirm 0 hits, or leftovers are all **historical narrative** (comments quoting old code, dated records).
Example: after a tree rename, 8 scripts still wrote the old path (3 of them with `cd … || exit`, so they wouldn't even run).

**D3 Dangling references**
After moving/deleting files, search for references; index-style docs get the line deleted or rewritten as a **pointer to the new location**.
Example: after notes moved into archive, the two index lines had to become "archived with the line to …".

**D4 Verdict contradicts the implementation's direction**
With a two-state verdict the reason field says "missing data"; don't write ❌ and "not judged fail" in the same sentence (readers will treat it as a third value).
Example: a single sentence containing both "❌" and "**not judged fail**".

**D5 Motivation sentences rot**: in comments/docs "because X we do Y", where X is a **measurement** — once the measurement is overturned the motivation sentence rots last (nobody runs it)
`grep` the new code and docs for **numbers and "whys"**, check each against the latest measurement table.
Example: batching was motivated by "88 round trips = 7-15 ms"; measurement proved round-trip count wasn't the main factor (the real cause = queuing on the shared connection) — 9 comments and doc passages needed changing together, including a test docstring.

**D6 Disproved evidence left in docs** (fake fields / old-format log excerpts)
For each field in a pasted log excerpt, check "does this number still exist now"; replace dead evidence with a **pointer to where it landed**, don't re-copy.
Example: old-format timing lines carried three **always-zero fake fields** (initialized and never accumulated); leaving them in docs means treating fake evidence as conclusions.

## E. Cross-repo / cross-machine class

| #   | Symptom                                    | Quick check                            |
| --- | ------------------------------------------ | -------------------------------------- |
| E1  | Two copies of one source disagree          | Compare key sections or md5            |
| E2  | Coordinates and machine facts on defaults  | Each item points to prior-run evidence |
| E3  | Out-of-bounds edits into archived surfaces | Confirm not in the archive/frozen set  |

**E1 Two copies of one source disagree** (code / docs)
Compare the same key sections or md5 of the same file on both ends — don't compare "looks about the same".
Example: L2 code in a dual-source repo needs a per-item functional diff list.

**E2 Coordinates and machine facts left to defaults**
Tree names / images / BDF / IP each **point back to the evidence of the last comparable run**.
Example: the build chain's `DOCKER_IMAGE`/`REPO_DIR` passed explicitly, or at least cross-check the tag in the startup log.

**E3 Out-of-bounds edits into archived surfaces**
Confirm the change target is **not in the archived/frozen set** — archived material is not reviewed, not fixed, not run.
Example: adding version records for an archived branch, running an archived skill's self-verification suite.

## F. Commit-surface class

| #   | Symptom                                   | Quick fix                             |
| --- | ----------------------------------------- | ------------------------------------- |
| F1  | Path limiting off / swallowed staged work | Commit only the listed paths          |
| F2  | Rename committed as one half only         | Check the tree after committing       |
| F3  | Message got shortened                     | Message to disk first; reuse verbatim |
| F4  | Hook modified files and aborted           | Check %s keyword; add and retry       |
| F5  | Staged work downgraded by history rewrite | Save patch first; add back and cmp    |
| F6  | Mutation writes through to repo files     | Mutate copies only; verify both ends  |

**F1 Path limiting not in effect / swallowed someone else's staged work**
`git commit -F msg -- <paths>` carries **only the listed paths**; **untracked files must be `git add`ed first** (otherwise "did not match any Git-known files").

**F2 Rename committed as one half only**
After `git mv`, `git commit -- <new-name>` carrying only the new side ⇒ HEAD holds both old and new. Criterion = check the **tree** after committing: `git ls-tree HEAD --name-only | grep <old-name>` should be 0; repair with a commit carrying the old path.

**F3 Message got shortened**
The message **goes to disk first** (`Write /tmp/<batch>-msg.txt`) then `git commit -F`; when retrying after a hook abort, **reuse the same file verbatim** — retyping tends to shrink it, and the short version lands in history (criterion: `git log -1 --format=%B | wc -l`).

**F4 Hook modified files and aborted the commit**
Criterion = after committing `git log -1 --format=%s`, retry if the keyword didn't land; `git add` the hook-modified files and commit again, **no `--no-verify`**.

**F5 Staged work downgraded while rewriting history**
`rebase --autostash` restores **staged** changes to unstaged (content survives) ⇒ beforehand `git diff --cached > /tmp/staged.patch` + note the path list; afterwards `git add` them back and `cmp` to verify byte-identical restoration.

**F6 Mutation self-check writes through to repo files** (the "read-only" mutation copy actually wrote the real file)
Mutate **only on copies** (`cp` to `/tmp/<dir>` first), or `rm` the symlink before writing a regular file — `open(path,"w")` **writes through symlinks** into the target; overlay/link-farm setups are the most exposed. **Check once before and once after the mutation**: `git diff --stat`, `git status --short`, and key-file md5 must match the pre-incident values exactly ("looks restored" doesn't count — the numbers must match); if it slipped ⇒ `git show HEAD:<path>` for exact restoration + re-run the mechanical gates and affected tests.
Example: a proofreading agent mutated via a symlink overlay, and `open(...,"w")` wrote through into two core source files of the real repo (deleting a commit loop along the way); it claimed restoration ⇒ independent re-verification via md5 and `git diff --stat`, item by item, was what confirmed no residue.
