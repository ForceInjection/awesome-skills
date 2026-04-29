#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <input.png> <output.png> [bg_hex] [tolerance] [--bottom N]" >&2
  echo "  bg_hex:    background color in hex, default ffffff" >&2
  echo "  tolerance: RGB variance threshold, default 10" >&2
  echo "  --bottom N: trim exactly N pixels from bottom (bypasses auto-detect)" >&2
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

input_path=$1
output_path=$2
shift 2

bg_hex="ffffff"
tolerance="10"
bottom_trim=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bottom)
      if [[ $# -lt 2 ]]; then
        echo "Error: --bottom requires a value" >&2
        usage
      fi
      bottom_trim="$2"
      shift 2
      ;;
    *)
      if [[ "$bg_hex" == "ffffff" && "$1" != "" ]]; then
        bg_hex="$1"
      elif [[ "$tolerance" == "10" && "$1" != "" ]]; then
        tolerance="$1"
      fi
      shift
      ;;
  esac
done

if [[ ! -f "$input_path" ]]; then
  echo "Input PNG not found: $input_path" >&2
  exit 1
fi

mkdir -p "$(dirname "$output_path")"

python3 - "$input_path" "$output_path" "$bg_hex" "$tolerance" "$bottom_trim" << 'PYEOF'
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
bottom_trim = sys.argv[5]

img = Image.open(input_path)
if img.mode != "RGB":
    img = img.convert("RGB")

width, height = img.size

# Fixed bottom trim mode (e.g., --bottom 10)
if bottom_trim:
    trim_px = int(bottom_trim)
    if trim_px >= height:
        print(f"Error: trim amount ({trim_px}) >= image height ({height})", file=sys.stderr)
        sys.exit(1)
    trim_y = height - trim_px
    trimmed = img.crop((0, 0, width, trim_y))
    trimmed.save(output_path)
    print(f"Trimmed {trim_px}px from bottom. Saved to {output_path}")
    sys.exit(0)

# Auto-detect mode: scan from bottom to find first non-background row
bg_hex = bg_hex.lstrip("#")
bg_color = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))

pixels = img.load()

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
