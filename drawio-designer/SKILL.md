---
name: "drawio-designer"
description: "Creates, edits, and manages draw.io XML diagrams, converts them to PNG, and integrates AWS, K8s, and General IT icons. Invoke when the user wants to create, modify, or format draw.io architecture diagrams or flowcharts."
---

# drawio-designer Diagram Skill

A Claude Code / Trae AI skill for creating, editing, and managing draw.io diagrams with professional quality standards.

## Purpose

This skill enables AI-assisted creation and maintenance of draw.io architecture diagrams, flowcharts, and technical documentation visuals. It ensures consistent styling, proper layout, and automated PNG conversion for presentations and documentation.

## When to Use This Skill

Use this skill when you need to manipulate diagram assets or layout structures programmatically. The core scenarios cover XML modifications, format conversions, and layout adjustments:

- Create or edit `.drawio` XML diagram files
- Convert diagrams to PNG format with transparent backgrounds
- Adjust element positions and layouts programmatically
- Ensure consistent font families (especially for Quarto slides)
- Work with architecture diagrams using official AWS, Kubernetes, and General IT icons
- Maintain professional diagram quality with accessibility standards
- Debug layout issues or element overlaps

## How It Works

The skill provides direct XML manipulation and automated quality checks to ensure diagrams meet professional standards. The operational workflow includes:

- **Direct XML Editing**: Manipulates `.drawio` files as structured XML
- **Automated Conversion**: Converts diagrams to high-resolution PNG via scripts
- **Layout Calculations**: Computes proper spacing, alignment, and margins
- **Icon Integration**: Searches and integrates official architecture icons (AWS, K8s, Network, General)
- **Quality Assurance**: Applies design principles and accessibility guidelines

## Key Features

The capabilities of this skill ensure high-fidelity outputs for complex architectures and technical flows.

### Font Management

Typography consistency across diagrams is enforced by strict styling rules:

- Sets `defaultFontFamily` in `mxGraphModel`
- Applies `fontFamily` to individual text elements
- Recommended: `"Noto Sans JP"` for Japanese text support

### PNG Conversion

Conversion tools produce optimized images tailored for documentation:

- 2x scale (high resolution)
- Transparent background
- PNG format suitable for presentations

### Layout Adjustment

Programmatic element positioning ensures alignment and prevents overlapping:

- Calculate element centers: `y + (height / 2)`
- Align multiple elements by matching center coordinates
- Maintain minimum 30px margins from container boundaries
- Position arrows to avoid label overlaps (20px+ clearance)

### Visual Styling (Edges & Icons)

To ensure diagrams render correctly across all platforms and PNG conversions, you must enforce strict styling rules:

- **Edges (Connections)**: ALWAYS explicitly define `strokeColor` and `strokeWidth` in the style (e.g., `style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#333333;strokeWidth=2;html=1;"`). Without this, lines may render invisibly.
- **Edge Labels**: Labels must be separate `<mxCell>` elements with `vertex="1" connectable="0" parent="[edge_id]"` rather than being properties of the edge itself.
- **Label Overlap Prevention**: Icons typically use `verticalLabelPosition=bottom`. Vertical connections exiting from the bottom will cross and obscure this text. To prevent overlap, explicitly route connections from the sides using `exitX`, `exitY` (e.g., `exitX=0;exitY=0.5;exitDx=0;exitDy=0` for the left side) and define an `<Array as="points">` in the `mxGeometry` to route the edge clearly around the text.
- **Icons**: Ensure `html=1` and `pointerEvents=1` are included in the style. AWS 4 resource icons **MUST** include a `fillColor` matching their AWS category and `strokeColor=none`. Without `fillColor`, the SVG path will render as transparent/invisible in CLI exports!
  - _Compute_ (e.g., EC2, ECS, Lambda): `fillColor=#F58536`
  - _Database_ (e.g., RDS, DynamoDB): `fillColor=#3355CC`
  - _Networking_ (e.g., VPC, API Gateway): `fillColor=#8C4FFF`
  - _Storage_ (e.g., S3): `fillColor=#4F81A1`
  - _General/Default_: `fillColor=#232F3E`
  - Example: `style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#F58536;strokeColor=none;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"`

### Architecture Icon Integration

Search and integrate official architecture service icons using the built-in script. It supports standard AWS resources (`mxgraph.aws4.*`), Kubernetes objects (`img/lib/kubernetes/*`), Network topology elements (`mxgraph.cisco.*`), and General IT elements (databases, actors, clouds) with automated styling.

### Design Principles

Professional standards are applied to every diagram modification to guarantee clarity:

- **Clarity**: Simple, visually clean diagrams
- **Consistency**: Unified colors, fonts, icon sizes, line thickness
- **Accuracy**: Precise technical representation
- **Accessibility**: Sufficient color contrast, pattern usage
- **Progressive Disclosure**: Staged diagrams for complex systems

### Quality Checklist

Automated validation ensures diagrams pass all baseline layout checks:

- No background color (transparent)
- Appropriate font sizes (1.5x standard for readability)
- Arrows on back layer (no overlaps)
- 30px+ margins from container boundaries
- Official service names and latest icons (AWS, K8s, Network, General)
- Visual verification of PNG output

## Usage Examples

The following patterns demonstrate the standard approach for creating, converting, and searching for diagram components.

### Create AWS Architecture Diagram

```xml
<!-- Set font family to ensure text consistency -->
<mxGraphModel defaultFontFamily="Noto Sans JP">

  <!-- Background frame with proper margins -->
  <mxCell id="vpc" style="rounded=1;strokeWidth=3;...">
    <mxGeometry x="500" y="20" width="560" height="430" />
  </mxCell>

  <!-- Title with 30px margin from frame top -->
  <mxCell id="title" value="VPC" style="text;fontSize=18;fontFamily=Noto Sans JP;">
    <mxGeometry x="510" y="50" width="540" height="35" />
  </mxCell>

  <!-- API Gateway -->
  <mxCell id="api_gateway" value="API Gateway" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;fillColor=#232F3E;strokeColor=none;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;" vertex="1" parent="1">
    <mxGeometry x="360" y="160" width="80" height="80" as="geometry" />
  </mxCell>

  <!-- Arrow with explicit coordinates for accurate pointing -->
  <mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#333333;strokeWidth=2;html=1;" edge="1" parent="1" source="vpc" target="api_gateway">
    <mxGeometry relative="1" as="geometry" />
  </mxCell>

  <!-- Arrow label with offset to avoid overlap -->
  <mxCell id="label1" value="API Request" style="edgeLabel;fontSize=14;fontFamily=Noto Sans JP;html=1;align=center;verticalAlign=middle;resizable=0;points=[];" vertex="1" connectable="0" parent="arrow1">
    <mxGeometry x="0" y="-20" relative="1" as="geometry">
      <mxPoint as="offset"/>
    </mxGeometry>
  </mxCell>
</mxGraphModel>
```

### Convert Diagram to PNG

```bash
# Convert to PNG using the provided script
bash scripts/drawio-to-png.sh architecture.drawio
# Result: architecture.png (2x resolution, transparent)
```

### Find Architecture Icon

```bash
# Search for EC2 icon string reference
python scripts/find-arch-icon.py ec2
# Output: mxgraph.aws4.ec2

# Search and get the complete style string including standard category color
python scripts/find-arch-icon.py ec2 --style
# Output: shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#F58536;strokeColor=none;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;

# Search for Kubernetes Pod style
python scripts/find-arch-icon.py pod --style
# Output: shape=image;image=img/lib/kubernetes/compute/pod.svg;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;

# Search for Network Router style
python scripts/find-arch-icon.py router --style
# Output: shape=mxgraph.cisco.routers.router;fillColor=#ffffff;strokeColor=#036897;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;

# Search for General Database style
python scripts/find-arch-icon.py database --style
# Output: shape=cylinder3;fillColor=#dae8fc;strokeColor=#6c8ebf;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;
```

## Best Practices

**Text Width Calculation**
Japanese text requires 30-40px per character to render correctly without clipping:

```xml
<!-- For 10-character text: 300-400px width allocated -->
<mxGeometry x="140" y="60" width="400" height="40" />
```
