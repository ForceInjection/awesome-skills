---
name: pptx-editor
description: Precisely edit PowerPoint (.pptx) files — locate shapes by semantic name for run-level text replacement and styled element insertion, then verify with LibreOffice + pdftotext rendering (no overflow, no collisions). Use when the user asks to modify, edit, or update the text, layout, or elements of an existing .pptx deck.
---

# PPTX Editor Skill

This document defines the standard workflow for **precise, verifiable modifications** to existing `.pptx` files. Complementary to [pptx-reader](../pptx-reader/SKILL-en.md): the reader extracts and analyzes; this skill modifies and verifies.

Core principle: **no render, no verify**. This skill assumes the execution environment cannot view images directly, so every layout conclusion is based on rendered word-level coordinates.

## 1. Quick Reference

| Task | How |
| --- | --- |
| Recon before editing | `python3 scripts/dump.py file.pptx --slides 2,20` (lists each shape's name / geometry / font / text) |
| Text replacement / inserting elements | Write a one-off patch script (template `scripts/patch_template.py`); run-level replacement with paragraph-level fallback, printing OK/MISS per item |
| Render verification | `python3 scripts/verify.py file.pptx` (LibreOffice → PDF → pdftotext -bbox → full-page overflow scan; exit code 0 = pass) |
| Band-gap / collision check | Word-level bbox coordinates + unique per-element marker words (see §4.2) |

## 2. Environment Setup

Dependencies: `python3` + `python-pptx`, LibreOffice (`soffice`), poppler (`pdftotext` / `pdfinfo`).

- macOS: `soffice` lives at `/Applications/LibreOffice.app/Contents/MacOS/soffice`; the scripts auto-detect it.
- If `python-pptx` is missing, create a venv inside the skill's `scripts/` directory: `python3 -m venv venv && venv/bin/pip install python-pptx`.
- The PDF render uses **substituted fonts** (e.g. MiSans → fallback), so line heights differ slightly from PowerPoint/Keynote — leave generous margins per the empirical values in §5.

## 3. Edit Workflow

1. **Recon**: `dump.py` lists every shape on the target slides. Shapes in our decks have semantic names (e.g. `p20_shift`, `f2_src`) — **locate by shape name**, never by blind text search within a slide.
2. **Patch**: write `/tmp/fix_ppt_*.py` from the template; one patch = one coherent group of changes; the script prints `OK xN / MISS` per item — done only when everything is OK.
3. **Verify**: `verify.py` full-page overflow scan; when inserting or moving elements, also run the band-gap check (§4.2).
4. **Report**: tell the user how each change was located and verified; if you find a pre-existing bug (e.g. text clipped off the slide), report it honestly and fix it.

## 4. Patch Methods (python-pptx)

### 4.1 Text Replacement: Run-Level First, Paragraph-Level Fallback

- **Run-level**: when `old in r.text`, do `r.text = r.text.replace(old, new)` — preserves that run's font formatting.
- **Paragraph-level fallback**: when a sentence is split across runs, concatenate all run text, match, write the result back into the first run and clear the rest (preserving the first run's format).
- Common template functions: `rep_runs()` / `replace_in_paragraph()` in `scripts/patch_template.py`.

### 4.2 Inserting Elements: Copy the Style of Neighboring Elements

Before adding a text box, query the actual parameters of a similar element on the same slide with `dump.py` and copy them item by item:

- `font.name` (MiSans in our decks), `font.size`, `font.bold`, `font.color.rgb`
- `tf.margin_* = 0`, `tf.word_wrap`, `tf.vertical_anchor` (MIDDLE/TOP), `p.line_spacing`
- Positions in decimal inches (e.g. `Inches(4.36)`), aligned to the slide's existing grid

Template function: `add_text()` in `patch_template.py`.

### 4.3 Geometry and Typography Adjustments

- Position/size: `shape.top = Inches(x)`, `shape.height = Inches(h)`
- Wrapping: `shape.text_frame.word_wrap = True/False`
- Line spacing: `paragraph.line_spacing = 1.0` (default 1.2–1.35)

## 5. Verification (Headless Environment)

### 5.1 Overflow Scan (mandatory after every edit)

`verify.py`: LibreOffice headless → PDF → `pdftotext -bbox` word coordinates → check for words beyond the page edges (**anything over the edge is clipped** — PPT does not reflow or narrow text).

### 5.2 Band-Gap / Collision Check

When several elements stack vertically, use **unique per-element words** as markers to locate each element and measure the gap between bands:

```python
import re, subprocess
subprocess.run(["pdftotext","-f",str(pg),"-l",str(pg),"-bbox",pdf,out], check=True)
words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>',
                   open(out, encoding="utf-8").read())
def band(ws): return (min(float(w[1]) for w in ws), max(float(w[3]) for w in ws))
cap = [w for w in words if "拉平" in w[4]]          # marker: a word unique to the element
shift = [w for w in words if "价值正在" in w[4]]
gap = band(shift)[0] - band(cap)[1]                 # negative = collision
```

Marker-selection pitfall: avoid words that also appear in other elements (e.g. `$150` may show up in both a title and a chart); when a marker hits multiple matches, filter again by coordinates (y-range).

## 6. Lessons and Pitfalls (distilled from real edit cases)

1. **`wrap="none"` is a ticking time bomb**: appended text will not wrap and spills past the slide's right edge, clipped (once hid an entire sentence "…跨境流。"). After appending text, check `word_wrap` and re-render to confirm.
2. **Line-height estimates** (LibreOffice fallback fonts): ≈ font-size × 1.32 per line (≈ ×1.21 with line_spacing 1.0). Keep ≥5pt between bands, because PowerPoint/Keynote render with real fonts and differ slightly.
3. **Single-line width estimates**: at 12pt, CJK ≈ 12pt/char, Latin/digits ≈ 6.4–6.9pt/char. A 13.33" slide gives ≈ 832pt of usable width; anything beyond wraps.
4. **Wrapping triggers cascading collisions**: extra lines × line height eat into the element below. Count lines before adding text, then set size/box height.
5. **Font-substitution drift**: verification uses substituted fonts whose line heights only grow — if the render passes, the real environment (more compact) passes too.
6. **.pptx files are often gitignored** (as in this repo): confirm the file is a local working draft before editing; back up important versions first.
7. **One patch = one coherent group of changes**, each item printing OK/MISS; never batch unrelated changes — a MISS then can't be localized.

## 7. Dependencies

- `python-pptx`: read/write .pptx.
- LibreOffice (`soffice`): headless PDF conversion for render verification.
- poppler (`pdftotext`, `pdfinfo`): extract word-level coordinates from PDFs.
