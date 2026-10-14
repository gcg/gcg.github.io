#!/bin/bash
set -e

# Test 1: Mobile CSS wrap & overflow rules
grep -A 5 "social-links-row" assets/css/style.css | grep -q "flex-wrap: wrap" || { echo "Missing flex-wrap on social-links-row"; exit 1; }
grep -A 10 "hunter-class-badge" assets/css/style.css | grep -q "max-width: 100%" || { echo "Missing max-width on hunter-class-badge"; exit 1; }
grep -A 5 "footer-credit" assets/css/style.css | grep -q "flex-wrap: wrap" || { echo "Missing flex-wrap on footer-credit"; exit 1; }

# Test 2: Interactive portrait scanning CSS rule
grep -q "portrait-container.scanning" assets/css/manhwa.css || { echo "Missing .portrait-container.scanning CSS rule"; exit 1; }

# Test 3: Beacon focus listeners and interval clearing
grep -q "focusin" assets/js/rotating-id.js || { echo "Missing focusin listener in rotating beacon"; exit 1; }
grep -A 5 "pause()" assets/js/rotating-id.js | grep -q "clearInterval" || { echo "Missing clearInterval in pause()"; exit 1; }

# Test 4: Git working tree clean (README committed)
git status --porcelain | grep -q "README" && { echo "README still modified in git status"; exit 1; } || true

echo "Final review fix pass verification passed!"
