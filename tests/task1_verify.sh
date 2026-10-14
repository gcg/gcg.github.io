#!/bin/bash
set -e
test -f assets/img/gcg.jpg || { echo "Missing gcg.jpg"; exit 1; }
test -f assets/favicons/favicon.ico || { echo "Missing favicon.ico"; exit 1; }
grep -q "python3 -m http.server" Makefile || { echo "Makefile missing python http server"; exit 1; }
echo "Task 1 verification passed"
