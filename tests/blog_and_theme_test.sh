#!/bin/bash
set -e

# Test 1: Favicon SVG with gcg
test -f assets/favicons/favicon.svg || { echo "Missing favicon.svg"; exit 1; }
grep -q "gcg" assets/favicons/favicon.svg || { echo "favicon.svg missing gcg text/glyph"; exit 1; }

# Test 2: Light mode tokens in variables.css
grep -q '\[data-theme="light"\]' assets/css/variables.css || { echo "Missing [data-theme=light] in variables.css"; exit 1; }

# Test 3: Theme switcher script
test -f assets/js/theme-toggle.js || { echo "Missing theme-toggle.js"; exit 1; }

# Test 4: Blog / Chronicles section in index.html
grep -q "Hunter Chronicles" index.html || { echo "Missing Hunter Chronicles in index.html"; exit 1; }
grep -q "Technologies I Am Investing in 2024" index.html || { echo "Missing 2024 post in index.html"; exit 1; }
grep -q "Technologies I Am Investing in 2023" index.html || { echo "Missing 2023 post in index.html"; exit 1; }
grep -q "My New Neovim Setup with 100% Lua" index.html || { echo "Missing Neovim post in index.html"; exit 1; }
grep -q "Hello Hugo" index.html || { echo "Missing Hello Hugo post in index.html"; exit 1; }

# Test 5: Theme toggle button in index.html
grep -q "theme-toggle" index.html || { echo "Missing theme-toggle button in index.html"; exit 1; }

# Test 6: Full background coverage for light mode
grep -q "var(--bg-primary)" assets/css/reset.css || { echo "reset.css missing var(--bg-primary)"; exit 1; }
grep -q "\-\-bg-nav:" assets/css/variables.css || { echo "variables.css missing --bg-nav definition"; exit 1; }
grep -q "var(--bg-nav)" assets/css/style.css || { echo "style.css missing var(--bg-nav)"; exit 1; }
grep -q '\[data-theme="light"\] \.code-syntax-backdrop' assets/css/style.css || { echo "style.css missing light mode syntax backdrop"; exit 1; }
grep -q '\[data-theme="light"\] \.chronicle-prose pre' assets/css/style.css || { echo "style.css missing light mode pre styles"; exit 1; }

echo "Blog and theme test passed!"

