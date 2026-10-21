#!/usr/bin/env bash
# One-off: cuts the self-hosted fonts in assets/fonts/ down to the characters the site uses.
# Re-run after adding Chinese text to index.html or templates/post.html.
# Needs fonttools + brotli (for woff2):
#   python3 -m venv /tmp/fontvenv && /tmp/fontvenv/bin/pip install fonttools brotli
#   FONTTOOLS=/tmp/fontvenv/bin/pyftsubset scripts/subset_fonts.sh
# Source TTFs (OFL) come from https://github.com/google/fonts (ofl/<family>/) and live in $SRC.
set -euo pipefail

cd "$(dirname "$0")/.."
PYFTSUBSET="${FONTTOOLS:-pyftsubset}"
SRC="${SRC:-.superpowers/redesign-assets/fonts-src}"
OUT=assets/fonts
mkdir -p "$OUT"

# Every CJK character used on the site (homepage + post template).
CJK=$(python3 -c '
import re, sys
text = "".join(open(p, encoding="utf-8").read() for p in sys.argv[1:])
print("".join(sorted(set(re.findall(r"[　-鿿＀-￯]", text)))))
' index.html templates/post.html)

"$PYFTSUBSET" "$SRC/MaShanZheng-Regular.ttf" --text="${CJK}!?· " \
  --flavor=woff2 --layout-features='*' --output-file="$OUT/ma-shan-zheng.woff2"

LATIN="U+0000-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2190-2193,U+2197,U+20AC"
latin() {
  "$PYFTSUBSET" "$SRC/$1" --unicodes="$LATIN" --flavor=woff2 --layout-features='*' --output-file="$OUT/$2"
}
latin Cinzel.ttf cinzel.woff2
latin CormorantGaramond.ttf cormorant-garamond.woff2
latin CormorantGaramond-Italic.ttf cormorant-garamond-italic.woff2
# Shantell Sans is only used bold (800); pin its four axes to keep the file small.
TOOLS_BIN="$(dirname "$(command -v "$PYFTSUBSET")")"
"$TOOLS_BIN/fonttools" varLib.instancer "$SRC/ShantellSans.ttf" wght=800 BNCE=0 INFM=0 SPAC=0 \
  --output="$SRC/ShantellSans-800.ttf" >/dev/null
latin ShantellSans-800.ttf shantell-sans.woff2
latin JetBrainsMono.ttf jetbrains-mono.woff2

ls -l "$OUT"
