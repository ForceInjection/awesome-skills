---
name: pptx-reader
description: "Understand, read, and analyze the content of .pptx slide files. Invoke this skill when the user needs to extract PPT text or analyze a presentation."
---

# PPTX Reader Skill

This document details how to use this skill to read and parse .pptx files. Data and best practices are referenced from the [anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) repository on GitHub.

## 1. Quick Reference

Extract the slide deck's core text content in a single command using the markitdown CLI tool — ideal for fast data ingestion scenarios.

| Task            | Guide                                                                 |
| --------------- | -------------------------------------------------------------------- |
| Read / analyze content | Run `python -m markitdown presentation.pptx > output_dir/output.md` |

## 2. Environment Setup

To avoid dependency conflicts and restrictions from externally managed environments, run all parsing scripts inside a dedicated Python virtual environment.

On macOS and similar systems, a virtual environment is strongly recommended to avoid conflicts with the system-wide Python (e.g., the `externally-managed-environment` error).

```bash
# Enter the scripts directory
cd scripts

# Create a virtual environment named venv
python3 -m venv venv

# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Install the required dependencies
pip install "markitdown[pptx]" Pillow defusedxml
```

## 3. Read Content

Use Python scripts to extract a plain-text stream directly from .pptx files, generate multi-slide visual overviews, or unpack the raw XML structure for deep review.

Make sure the virtual environment in the `scripts` directory is activated, then run the following commands:

```bash
# Create a unified output directory
mkdir -p output_dir

# Extract the plain-text content from the PPTX and write it to the specified file
python -m markitdown presentation.pptx > output_dir/output.md

# Generate a visual overview of the specified PPTX file, with the given output prefix (including directory)
python thumbnail.py presentation.pptx output_dir/thumbnails

# Unpack the PPTX file into the specified unpacked directory
python office/unpack.py presentation.pptx output_dir/unpacked/
```

## 4. Convert to Images

Use the LibreOffice and Poppler toolchain to render the presentation losslessly to PDF and split it page by page into high-resolution JPEG images, providing source material for multimodal visual analysis by large models.

Convert the presentation to individual slide images for visual inspection:

```bash
# Create a unified output directory
mkdir -p output_dir

# Convert the PPTX file to PDF in headless mode, outputting to the specified directory
python office/soffice.py --headless --convert-to pdf --outdir output_dir/ presentation.pptx

# Convert the generated PDF into a sequence of JPEG images at 150 DPI, with the given output prefix (including directory)
pdftoppm -jpeg -r 150 output_dir/presentation.pdf output_dir/slide
```

This generates files such as `output_dir/slide-01.jpg`, `output_dir/slide-02.jpg`, etc., ready to be fed to a large language model for visual layout analysis.

## 5. Dependencies

Text extraction, image rendering, and unpacking rely on the following Python packages and system-level CLI tools.

- **`markitdown[pptx]`**: Text extraction.
- **`Pillow`**: Thumbnail grid generation.
- **`defusedxml`**: Safe XML parsing (thumbnail slide-information extraction and unpacking).
- **LibreOffice (`soffice`)**: PDF conversion (auto-configured in sandbox environments via `office/soffice.py`; `run_soffice` automatically injects a temporary user profile to avoid the "User installation could not be completed" crash in sandboxes).
- **Poppler (`pdftoppm`)**: PDF-to-image conversion.
