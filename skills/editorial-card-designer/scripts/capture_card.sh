#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <input.html> <output.png> <ratio>" >&2
  exit 1
fi

input_path=$1
output_path=$2
ratio_key=$3

case "$ratio_key" in
  "3:4")
    width=1500
    height=2000
    ;;
  "4:3")
    width=2000
    height=1500
    ;;
  "1:1")
    width=1800
    height=1800
    ;;
  "16:9")
    width=1920
    height=1080
    ;;
  "9:16")
    width=1080
    height=1920
    ;;
  "2.35:1")
    width=2350
    height=1000
    ;;
  "3:1")
    width=1800
    height=600
    ;;
  "5:2")
    width=2500
    height=1000
    ;;
  *)
    echo "Unsupported ratio: $ratio_key" >&2
    echo "Supported ratios: 3:4, 4:3, 1:1, 16:9, 9:16, 2.35:1, 3:1, 5:2" >&2
    exit 1
    ;;
esac

resolve_chrome_bin() {
  if [[ -n "${CHROME_BIN:-}" ]]; then
    if [[ -x "$CHROME_BIN" ]]; then
      echo "$CHROME_BIN"
      return 0
    fi
    echo "CHROME_BIN set but not executable: $CHROME_BIN" >&2
    return 1
  fi

  local candidates=(
    "google-chrome"
    "google-chrome-stable"
    "chromium"
    "chromium-browser"
    "chrome"
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
  )

  local candidate chrome_path
  for candidate in "${candidates[@]}"; do
    if [[ "$candidate" == */* ]]; then
      # Absolute or relative filesystem path
      if [[ -x "$candidate" ]]; then
        echo "$candidate"
        return 0
      fi
    else
      # PATH-based lookup; type -P ignores aliases/functions and returns only external executables
      if chrome_path=$(type -P -- "$candidate" 2>/dev/null) && [[ -n "$chrome_path" ]]; then
        echo "$chrome_path"
        return 0
      fi
    fi
  done
  return 1
}

if ! chrome_bin=$(resolve_chrome_bin); then
  echo "Chrome binary not found." >&2
  echo "Tried: CHROME_BIN, google-chrome, google-chrome-stable, chromium, chromium-browser, chrome, macOS app paths." >&2
  echo "Set CHROME_BIN to a working Chrome/Chromium binary." >&2
  exit 1
fi

if [[ ! -f "$input_path" ]]; then
  echo "Input HTML not found: $input_path" >&2
  exit 1
fi

# realpath fails on non-existent files, so resolve the directory first
mkdir -p "$(dirname "$output_path")"
abs_input_path=$(realpath "$input_path")
abs_output_path="$(realpath "$(dirname "$output_path")")/$(basename "$output_path")"
# Encode spaces for file:// URL compliance
input_url="file://${abs_input_path// /%20}"

"$chrome_bin" \
  --headless=new \
  --disable-gpu \
  --hide-scrollbars \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=30000 \
  --force-device-scale-factor=1 \
  --font-render-hinting=none \
  --no-first-run \
  --no-default-browser-check \
  --disable-background-networking \
  --window-size="${width},$((height + 120))" \
  --screenshot="$abs_output_path" \
  "$input_url"

if [[ ! -f "$abs_output_path" ]]; then
  echo "Screenshot failed: output file was not created." >&2
  exit 1
fi

echo "Saved screenshot to $abs_output_path"
