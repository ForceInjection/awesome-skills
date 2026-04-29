#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <input.png> <output.png> [bg_hex] [tolerance]" >&2
  echo "  bg_hex:    background color in hex, default ffffff" >&2
  echo "  tolerance: RGB variance threshold, default 10" >&2
  exit 1
fi

input_path=$1
output_path=$2
bg_hex=${3:-ffffff}
tolerance=${4:-10}

if [[ ! -f "$input_path" ]]; then
  echo "Input PNG not found: $input_path" >&2
  exit 1
fi

mkdir -p "$(dirname "$output_path")"

python3 - "$input_path" "$output_path" "$bg_hex" "$tolerance" << 'PYEOF'
import sys

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]
bg_hex = sys.argv[3]
tolerance = int(sys.argv[4])

# Parse background color
bg_hex = bg_hex.lstrip("#")
bg_color = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))

img = Image.open(input_path)
if img.mode != "RGB":
    img = img.convert("RGB")

width, height = img.size
pixels = img.load()

# Scan from bottom to find first non-background row
trim_y = height
for y in range(height - 1, -1, -1):
    is_bg = True
    for x in range(width):
        r, g, b = pixels[x, y]
        if (abs(r - bg_color[0]) > tolerance or
            abs(g - bg_color[1]) > tolerance or
            abs(b - bg_color[2]) > tolerance):
            is_bg = False
            break
    if not is_bg:
        trim_y = y + 1
        break

# Safety: never crop below 30% of original height
min_height = int(height * 0.3)
if trim_y < min_height:
    trim_y = height

if trim_y < height:
    trimmed = img.crop((0, 0, width, trim_y))
    trimmed.save(output_path)
    removed = height - trim_y
    print(f"Trimmed {removed}px from bottom ({removed / height * 100:.1f}%). Saved to {output_path}")
else:
    img.save(output_path)
    print(f"No trim needed. Saved to {output_path}")
PYEOF
