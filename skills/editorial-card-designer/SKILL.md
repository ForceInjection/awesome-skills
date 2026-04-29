---
name: editorial-card-designer
description: "Design high-density editorial HTML info cards in a modern magazine and Swiss-international style, then render them as ratio-specific PNG screenshots. Use when the user provides text or core information and wants: (1) a complete responsive HTML info card, (2) the design to follow the stored editorial prompt, (3) output in fixed visual ratios such as 3:4, 4:3, 1:1, 16:9, 9:16, 2.35:1, 3:1, or 5:2, or (4) both HTML and a rendered PNG cover/card from the same content."
metadata:
  {
    "clawdbot":
      {
        "requires":
          {
            "bins": [
              "google-chrome",
              "google-chrome-stable",
              "chromium",
              "chromium-browser",
              "chrome"
            ],
            "optional":
              {
                "bins": ["python3"],
                "python": ["Pillow"],
                "notes": "python3 + Pillow are only required when running scripts/trim_card_bottom.sh"
              }
          }
      }
  }
---

# Editorial Card Designer

## Overview

Turn source text into a compact, high-contrast HTML information card that follows the user's editorial prompt, then render a screenshot in one of the supported aspect ratios.
The goal is not just density but editorial quality: clear hierarchy, strong visual anchors, and screenshot-stable rendering without accidental cropping or dead space.

Always preserve three output stages unless the user explicitly asks to skip one:

1. Write one sentence judging the information density as high, medium, or low.
2. Output the complete HTML with embedded CSS.
3. Self-check that body text remains readable on mobile.

## Workflow

### 1. Analyze Content Density

Choose layout strategy from the content itself:

- Use "big-character" composition when content is sparse and a single phrase, number, or hook can carry the page.
- Use a two-column or three-column editorial grid when content is dense and needs stronger hierarchy.
- Use oversized numbers, heavy rules, tinted blocks, and pull-quote scale to avoid dead space.
- Do not force dense content into evenly weighted tiles. Build primary blocks, secondary blocks, and lighter supporting blocks.
- Match structure to content type:
  - Ranking / recommendation content: allow asymmetric hero + structured list.
  - Tutorial / analysis / interpretation content: group into overview, core judgment, interpretation, boundary, and conclusion.

Before compressing content, first change the layout skeleton.

- Ratio changes should primarily change reading path, hierarchy, and module arrangement.
- Do not treat ratio changes as a reason to delete content by default.
- Only compress, group, or summarize when the current ratio cannot hold the content clearly after layout has already been restructured.

### 2. Apply the Stored Editorial Rules

Load [references/editorial-card-prompt.md](references/editorial-card-prompt.md) as the canonical source for the full typographic scale, spacing rhythm, decoration rules, and Chinese-facing prompt language. That file is authoritative; the bullets below are only the invariants the model must honor even if the reference is skipped.

Core invariants (do not override unless the user explicitly asks):

- Import the stored Google Fonts stack (`Noto Serif SC`, `Noto Sans SC`, `Oswald`, `Inter`) and always declare local fallback font stacks so headless rendering stays stable when remote fonts fail.
- Body text stays at `18px`–`20px`; meta/tag text never drops below `13px`.
- Favor a white (`#ffffff`) or near-white background with EMC Blue (`#0083cb`) as the primary accent, unless the user supplies another palette.
- Build three visual tiers per card — primary, secondary, and lighter support blocks — instead of equal-weight tiles.
- Default to the `Hybrid` style mode; only switch to `Bold` or `Refined` when the user asks.
- If the user supplies a title, keep it verbatim as the main headline. Move interpretation, summary, and framing into subtitle / deck / summary slots rather than silently rewriting the title.
- Do not inject personal signatures, avatars, or account handles unless the user explicitly requests branding.

For the full typographic scale (super-title `72–112px`, large title `48–64px`, etc.), spacing envelope, decoration palette, and per-ratio composition rules, defer to [references/editorial-card-prompt.md](references/editorial-card-prompt.md) instead of restating them here.

### 3. Choose the Right Layout Skeleton

Pick ratio-specific structure before writing final copy. See [references/recommended-skeletons.md](references/recommended-skeletons.md) for detailed reusable patterns per ratio.

Key heuristics:

- **`4:3`** — asymmetric left-right; heavy primary + narrower judgment stack + thin footer.
- **`3:4`** — cover-style hero + mixed-scale modules; avoid a single narrow column.
- **`1:1`** — one heavy quadrant + supporting blocks; avoid four equal tiles.
- **Wide covers (`3:1`, `5:2`, `2.35:1`)** — fewer, larger blocks; aggressive paragraph reduction.

### 4. Build HTML for Rendering

When HTML will be screenshotted, design the page as a fixed-size canvas instead of a responsive webpage:

- Match the exact pixel dimensions of the selected ratio preset from `references/ratios.md`.
- Treat the card as a design board with explicit `width` and `height`, not as a fluid `100vw / 100vh` layout.
- Remove browser-default margins with `html, body { margin: 0; }`.
- Make the card itself fill the screenshot viewport exactly.
- Avoid interactions, sticky headers, or long scrolling sections.
- Use fixed pixel wrappers, for example:

  ```css
  .frame {
    width: 2000px;
    height: 1500px;
  }

  .card {
    width: 100%;
    height: 100%;
    padding: 48px;
    background: #ffffff;
  }
  ```

Do not rely on `100vw`, `100vh`, or responsive container widths as the primary design size for screenshot output.

If the user asks only for HTML, still make the layout screenshot-ready.

At the same time, preserve basic browser preview behavior:

- In screenshot mode, `html`, `body`, and the outer frame should match the target canvas size exactly.
- In mobile / narrow-width preview mode, add a media-query fallback that returns the page to normal flow so the HTML is still readable outside the screenshot workflow.

Use these structural heuristics when composing the card:

- Fill the proportion intentionally. Rebalance layout according to width / height instead of scaling one static template.
- Keep title, subtitle, summary, and modules separated by explicit rows or bands so they do not collide.
- When the user supplied the title, protect it as a first-class anchor. Expand the layout around it before you consider shortening or paraphrasing it.
- If using numbered modules, keep numbers visually weak enough that they never collide with titles.
- If a section becomes visually monotonous, introduce contrast through hierarchy changes rather than decorative clutter.
- Let big modules carry richer copy than small modules. Do not give every block the same amount of text.
- Do not use `1fr` rows or columns in ways that can create large accidental voids near the footer or push important content to the canvas edge.
- If the lower half feels empty, first rebalance module hierarchy or add a stronger bottom band before shrinking text or stretching containers.
- If a lower module is visually large, give it enough internal structure or a secondary judgment line so it earns the area it occupies.

### 5. Capture the Screenshot

Use the bundled shell script when the user wants a PNG output:

```bash
./scripts/capture_card.sh input.html output.png 3:4
```

Supported ratios and render sizes live in [references/ratios.md](references/ratios.md).

The rendering helper requires a local Chrome or Chromium binary.
It first respects `CHROME_BIN` when set, then falls back to common binary names and a macOS Chrome app path.

Before running the script:

- Save the generated HTML to a local file.
- Ensure the page is self-contained except for fonts.
- If you keep the default font imports, rendering will request Google Fonts over the network.
- Ensure the HTML uses a fixed-size design canvas that matches the chosen ratio preset.
- Ensure the viewport composition already matches the requested ratio.
- Ensure fallback fonts are declared so layout remains stable even if font downloads fail during headless rendering.

If the screenshot has bottom whitespace, improve the layout first. Only consider a slight aspect-ratio deviation as a last resort, and only when the user explicitly accepts it.

### 6. Ratio Policy

Accept only these ratio presets:

- `3:4`
- `4:3`
- `1:1`
- `16:9`
- `9:16`
- `2.35:1`
- `3:1`
- `5:2`

If the user gives a ratio outside this set, ask them to map it to the nearest supported preset rather than inventing a new one.

## Output Contract

When responding to a card-generation request:

- Start with exactly one sentence describing information density.
- Then output complete HTML in one code block.
- Self-check that body text remains readable on mobile.
- Self-check that the outer `frame`/canvas `width` and `height` in the HTML literally match the pixel preset for the chosen ratio in [references/ratios.md](references/ratios.md) before invoking the capture script. If they do not match, fix the HTML first — do not run the screenshot.
- If the user also requested an image, state the ratio used and the screenshot command after the HTML.
- Keep prose short; the HTML is the deliverable.

## Resources

### `references/ratios.md`

Open this when you need the exact preset names or capture dimensions.

### `references/editorial-card-prompt.md`

Use this as the canonical prompt spec when the user wants the latest validated editorial-card behavior.

### `references/recommended-skeletons.md`

Use this when you want ratio-specific reusable skeletons rather than one-off composition ideas.

### `scripts/capture_card.sh`

Run this to capture a PNG from a local HTML file using a supported ratio preset.
It requires a local Chrome or Chromium binary. The script resolves the binary in this order: `CHROME_BIN` env var → `google-chrome` / `google-chrome-stable` / `chromium` / `chromium-browser` / `chrome` on `PATH` → macOS `Google Chrome` / `Chromium` app paths. Set `CHROME_BIN` to override this auto-detection.

### `scripts/trim_card_bottom.sh`

Optional post-process. Trims bottom whitespace from a PNG by detecting the background color.
Requires Python 3 and Pillow (`pip install Pillow`).
Only use this when the user explicitly accepts a shorter image in exchange for removing bottom whitespace.

### `assets/card-template.html`

Use this as a starting shell when you want a minimal ratio-ready HTML canvas before filling in real content.
The template syncs its canvas size to the active viewport during capture, while still falling back to readable normal flow on narrower browser widths.

## Failure Checks

Before finalizing HTML or PNG, explicitly reject the result if any of these happen:

- A user-provided title was silently rewritten even though the ratio could have held it with a better layout.
- The title overlaps, visually collides with, or blocks summary/body content.
- The title becomes a narrow vertical strip when more horizontal width is available.
- Dense cards are split into too many equal-weight boxes.
- Large blocks contain too little copy and read like empty containers.
- The canvas shows large areas of dead space that could be filled by stronger hierarchy, richer block content, or a heavier main module.
- The PNG feels meaningfully emptier than the HTML layout intent.
- The rendered PNG uses a different reading rhythm than the HTML because remote fonts failed and no local fallback stack was provided.
- The footer or bottom band is cropped, or a large bottom whitespace strip appears because the grid sizing pushed content away from the lower edge.
