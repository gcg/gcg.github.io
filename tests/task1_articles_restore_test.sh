#!/bin/bash
set -e
test -f content/posts/technologies-i-am-investing-in-2024/index.md || exit 1
test -f content/posts/technologies-i-am-investing-in-2023/index.md || exit 1
test -f content/posts/neovim-lua/index.md || exit 1
test -f content/posts/neovim-lua/preview-2.png || exit 1
test -f content/posts/hello-hugo/index.md || exit 1
echo "Task 1 files verified"
