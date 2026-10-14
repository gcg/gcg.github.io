#!/bin/bash
set -e

# Test 1: Flanking stream classes in style.css
grep -q "code-stream-left" assets/css/style.css || { echo "Missing code-stream-left in style.css"; exit 1; }
grep -q "code-stream-right" assets/css/style.css || { echo "Missing code-stream-right in style.css"; exit 1; }

# Test 2: Flanking stream markup in index.html
grep -q "code-stream-left" index.html || { echo "Missing code-stream-left in index.html"; exit 1; }
grep -q "code-stream-right" index.html || { echo "Missing code-stream-right in index.html"; exit 1; }

# Test 3: Scroll synchronization in hunter-fx.js
grep -q "code-stream-left" assets/js/hunter-fx.js || { echo "hunter-fx.js missing left stream scroll binding"; exit 1; }
grep -q "code-stream-right" assets/js/hunter-fx.js || { echo "hunter-fx.js missing right stream scroll binding"; exit 1; }

echo "Backdrop scroll verification passed!"
