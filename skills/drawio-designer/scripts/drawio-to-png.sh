#!/bin/bash

# Simple wrapper script to convert .drawio XML files to PNG using draw.io CLI tools
# Installation:
# - macOS: brew install --cask drawio
# - Node: npm install -g drawio-batch

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path-to-diagram.drawio>"
    echo "This script attempts to convert a .drawio file to a transparent PNG."
    exit 1
fi

INPUT_FILE="$1"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found."
    exit 1
fi

# Use .png extension instead of .drawio.png if it ends in .drawio
OUTPUT_FILE="${INPUT_FILE%.drawio}.png"

# Detect drawio CLI executable path
if command -v drawio &> /dev/null; then
    DRAWIO_CMD="drawio"
elif command -v draw.io &> /dev/null; then
    DRAWIO_CMD="draw.io"
elif command -v drawio-batch &> /dev/null; then
    DRAWIO_CMD="drawio-batch"
elif [ -f "/Applications/draw.io.app/Contents/MacOS/draw.io" ]; then
    # Fallback to default macOS Homebrew Cask installation path
    DRAWIO_CMD="/Applications/draw.io.app/Contents/MacOS/draw.io"
else
    echo "Error: No draw.io CLI tools found. Cannot convert to PNG."
    echo "Please install drawio (e.g., 'brew install --cask drawio' on macOS)."
    exit 1
fi

echo "Converting $INPUT_FILE to $OUTPUT_FILE using $DRAWIO_CMD..."

# Execute conversion with transparency and 2x scale
# Quotes are used to handle paths containing spaces
"$DRAWIO_CMD" -x -f png --transparent --scale 2 -o "$OUTPUT_FILE" "$INPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Successfully generated: $OUTPUT_FILE"
else
    echo "Error: Conversion failed."
    exit 1
fi
