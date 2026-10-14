#!/bin/bash
set -e

# Test 1: Backdrop opacity in style.css is enhanced (no 0.09)
if grep -q "opacity: 0.09;" assets/css/style.css; then
  echo "Backdrop still using 0.09 opacity"; exit 1
fi
grep -q "opacity: 0.2" assets/css/style.css || { echo "Missing enhanced backdrop opacity"; exit 1; }

# Test 2: Full journey snippets in index.html
grep -q "Rails" index.html || { echo "Missing Rails snippet in index.html"; exit 1; }
grep -q "Laravel" index.html || { echo "Missing Laravel snippet in index.html"; exit 1; }
grep -q "Gleam" index.html || { echo "Missing Gleam snippet in index.html"; exit 1; }
grep -q "Fedora" index.html || { echo "Missing Linux/Fedora snippet in index.html"; exit 1; }
grep -q "OrchestrateInfra" index.html || { echo "Missing Go snippet in index.html"; exit 1; }

echo "Backdrop verification passed!"
