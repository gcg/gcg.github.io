#!/bin/bash
set -e
grep -q -- "--color-cyan" assets/css/variables.css || { echo "Missing --color-cyan"; exit 1; }
grep -q -- "--color-monarch" assets/css/variables.css || { echo "Missing --color-monarch"; exit 1; }
grep -q "system-window" assets/css/manhwa.css || { echo "Missing .system-window"; exit 1; }
grep -q "prefers-reduced-motion" assets/css/manhwa.css || { echo "Missing reduced motion query"; exit 1; }
echo "Task 2 CSS tokens verified"
