#!/bin/bash
set -e
grep -q "CHRONICLES_START" index.html || exit 1
grep -q "CHRONICLES_END" index.html || exit 1
grep -q "posts/technologies-i-am-investing-in-2024" index.html || exit 1
grep -q "Open Full Chronicle" index.html || exit 1
make build || exit 1
echo "Task 4 integration verified"
