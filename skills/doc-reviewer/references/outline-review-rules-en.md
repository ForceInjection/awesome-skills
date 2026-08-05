# Outline Review Rules (Structure Architect)

The core of this review type is **examining the logic and reasonableness of the section arrangement at a macro level**. Analyze all headings (the outline) of the document to ensure the document skeleton has a solid narrative structure and a good reading experience.

- **Logical Closure and Narrative Arc**: Evaluate whether the overall section arrangement forms a complete logical loop.
  - Check that the table of contents follows the standard narrative logic for the document type (e.g., tutorials: "basics → advanced → practice"; architecture docs: "background → architecture → modules → deployment"; troubleshooting: "symptom → analysis → solution → summary").
  - Ensure the document has a clear context introduction and a proper ending, avoiding logical gaps or abrupt chapter jumps.
- **Hierarchy and Containment Logic**:
  - Check heading levels (H1 → H2 → H3) for unreasonable jumps (e.g., H1 directly followed by H3).
  - Check that the containment between parent and child sections is strict (child section content must belong to its parent section).
- **Granularity and Weight Parity**: Check that sibling sections have comparable granularity; avoid one second-level section being enormous while a sibling section is extremely thin (consider demoting or splitting in such cases).
