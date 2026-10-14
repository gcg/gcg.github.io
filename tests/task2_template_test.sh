#!/bin/bash
set -e
test -f templates/post.html || exit 1
grep -q "{{title}}" templates/post.html || exit 1
grep -q "{{content}}" templates/post.html || exit 1
grep -q "{{formatted_date}}" templates/post.html || exit 1
grep -q "{{reading_time}}" templates/post.html || exit 1
grep -q "{{tags_html}}" templates/post.html || exit 1
grep -q "hud-back-btn" templates/post.html || exit 1
grep -q "theme-toggle-btn" templates/post.html || exit 1
echo "Task 2 template verified"
