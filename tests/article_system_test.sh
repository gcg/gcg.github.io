#!/bin/bash
set -e

PORT=8889

# 1. Run make build
make build || { echo "make build failed"; exit 1; }

# 2. Check generated files
for slug in technologies-i-am-investing-in-2024 technologies-i-am-investing-in-2023 neovim-lua hello-hugo; do
  file="posts/${slug}/index.html"
  test -f "$file" || { echo "Missing $file"; exit 1; }
  grep -q "hud-back-btn" "$file" || { echo "Missing hud-back-btn in $file"; exit 1; }
  grep -q "theme-toggle-btn" "$file" || { echo "Missing theme-toggle-btn in $file"; exit 1; }
  grep -q "theme-toggle.js" "$file" || { echo "Missing theme-toggle.js in $file"; exit 1; }
  grep -q "../../assets/css/style.css" "$file" || { echo "Missing style.css link in $file"; exit 1; }
done

# 3. Check Neovim image asset
test -s posts/neovim-lua/preview-2.png || { echo "Missing or empty posts/neovim-lua/preview-2.png"; exit 1; }

# 4. Check homepage links and target section ID
grep -q 'id="hunter-chronicles"' index.html || { echo "index.html missing id=hunter-chronicles"; exit 1; }
grep -q 'src="posts/neovim-lua/preview-2.png"' index.html || { echo "index.html preview image not re-based"; exit 1; }

for slug in technologies-i-am-investing-in-2024 technologies-i-am-investing-in-2023 neovim-lua hello-hugo; do
  grep -q "posts/${slug}/" index.html || { echo "index.html missing link to posts/${slug}/"; exit 1; }
done

# 5. Draft isolation test
mkdir -p content/posts/_test_draft
cat << 'EOF' > content/posts/_test_draft/index.md
---
title: "Classified Draft Chronicle"
date: 2026-10-14
draft: "true"
---
Secret hunter dispatch.
EOF

python3 scripts/build_posts.py
if [ -d "posts/_test_draft" ]; then
  echo "Draft post directory was incorrectly generated!"
  rm -rf content/posts/_test_draft
  exit 1
fi
if grep -q "Classified Draft Chronicle" index.html; then
  echo "Draft post was incorrectly listed on homepage!"
  rm -rf content/posts/_test_draft
  exit 1
fi
rm -rf content/posts/_test_draft

# 6. Local Server HTTP Verification
python3 -m http.server $PORT &
SERVER_PID=$!

cleanup() {
  kill $SERVER_PID 2>/dev/null || true
  wait $SERVER_PID 2>/dev/null || true
}
trap cleanup EXIT

sleep 1

# Curl 2024 post
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}/posts/technologies-i-am-investing-in-2024/")
if [ "$HTTP_CODE" != "200" ]; then
  echo "Expected 200 for article, got $HTTP_CODE"
  exit 1
fi

# Curl image asset
IMG_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}/posts/neovim-lua/preview-2.png")
if [ "$IMG_CODE" != "200" ]; then
  echo "Expected 200 for article image, got $IMG_CODE"
  exit 1
fi

echo "Article system end-to-end verification passed!"
