# drawio-designer Diagram Skill Reference

## Overview

This directory contains reference documentation for the `drawio-designer` skill. This skill allows Claude Code / Trae AI to properly construct and manage `.drawio` XML architecture diagrams, maintaining consistent typography, layout, and visual fidelity.

## Technical Details

The AI interacts with the raw `mxGraphModel` XML structure of a draw.io diagram.

Key considerations when the AI works with these files:

### Element Positioning

Draw.io uses absolute coordinates (`x`, `y`) and dimensions (`width`, `height`). AI must calculate relative positioning mathematically to avoid element overlap.

- Centers are typically calculated as `x + width/2` and `y + height/2`
- Edges (arrows) must attach to source/target points or define explicit entry/exit vectors.

### Architecture Icons

The `scripts/find-arch-icon.py` utility helps map common terminology (e.g. "EC2", "pod", "router", "database") to the specific draw.io style string (`shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#F58536...`). It supports AWS, Kubernetes, Network (Cisco), and General IT icons with strict style formatting required for headless rendering.

### PNG Conversion

Conversion is handled externally. It can be triggered via a `pre-commit` hook (if configured in the repository) or via the provided `scripts/drawio-to-png.sh` wrapper, which relies on standard CLI tools like `drawio-batch`.
