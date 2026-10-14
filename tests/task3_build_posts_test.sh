#!/bin/bash
set -e
python3 scripts/build_posts.py || exit 1
test -f posts/technologies-i-am-investing-in-2024/index.html || exit 1
test -f posts/technologies-i-am-investing-in-2023/index.html || exit 1
test -f posts/neovim-lua/index.html || exit 1
test -f posts/neovim-lua/preview-2.png || exit 1
test -f posts/hello-hugo/index.html || exit 1
grep -q "Technologies I Am Investing in 2024" posts/technologies-i-am-investing-in-2024/index.html || exit 1
grep -q "My New Neovim Setup with 100% Lua" posts/neovim-lua/index.html || exit 1
echo "Task 3 generator verified"
