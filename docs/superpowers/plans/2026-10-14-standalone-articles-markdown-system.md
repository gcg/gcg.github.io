# Standalone Articles & Markdown System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a zero-dependency Python 3 static site generator that compiles Markdown articles in `content/posts/` to standalone HTML pages at `/posts/<slug>/index.html` with Solo Leveling styling, syncs the homepage chronicle list, and integrates with `Makefile`.

**Architecture:** A standalone Python 3 script (`scripts/build_posts.py`) using only the standard library parses YAML frontmatter and Markdown syntax, copies local assets (e.g. images), populates `templates/post.html`, and syncs Chapter 04 chronicle cards in `index.html`. All output pages reuse the existing CSS tokens, theme switcher, and responsive manhwa styles.

**Tech Stack:** Python 3 (standard library only), HTML5, CSS3, vanilla ES6 JavaScript.

**Spec:** `docs/superpowers/specs/2026-10-14-standalone-articles-markdown-system-design.md`

## Global Constraints
- Zero external runtime or build dependencies (pure Python 3 standard library; no `pip install`).
- Target URLs must resolve to `/posts/<slug>/` (serving `/posts/<slug>/index.html`).
- Theme switcher compatibility: must support both dark mode (`#06070a` void) and light mode (`#f8fafc` awakening paper) with full viewport background coverage.
- Work strictly on branch `redesign-webtoon`; never push to `main`.
- All commands runnable via `make build` and `make serve`.

## Review Focus
- Fenced code blocks containing special characters (`<`, `>`, `&`) must be properly HTML-escaped so code doesn't break rendering.
- Relative image links within posts (like `preview-2.png` in `neovim-lua`) must copy to the destination post folder and render with HTTP 200.
- Draft posts (`draft: true`) must not be published to `posts/` or listed on the homepage.
- The `← Terminal` HUD link on post pages must navigate back smoothly to `../../#hunter-chronicles`.
- Markdown headings with punctuation or varying casing must generate valid, lowercase anchor IDs.

---

### Task 1: Restore Authentic Markdown Articles and Media

**Files:**
- Create: `content/posts/technologies-i-am-investing-in-2024/index.md`
- Create: `content/posts/technologies-i-am-investing-in-2023/index.md`
- Create: `content/posts/neovim-lua/index.md`
- Create: `content/posts/neovim-lua/preview-2.png`
- Create: `content/posts/hello-hugo/index.md`
- Test: `tests/task1_articles_restore_test.sh`

**Interfaces:**
- Produces: Source Markdown files with YAML frontmatter (`title`, `date`, `tags`, optional `draft`) and local image assets in `content/posts/`.

- [ ] **Step 1: Write the test verifying restored article files**

Create `tests/task1_articles_restore_test.sh`:
```bash
#!/bin/bash
set -e
test -f content/posts/technologies-i-am-investing-in-2024/index.md || exit 1
test -f content/posts/technologies-i-am-investing-in-2023/index.md || exit 1
test -f content/posts/neovim-lua/index.md || exit 1
test -f content/posts/neovim-lua/preview-2.png || exit 1
test -f content/posts/hello-hugo/index.md || exit 1
echo "Task 1 files verified"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/task1_articles_restore_test.sh`
Expected: FAIL (missing files)

- [ ] **Step 3: Extract the 4 markdown posts and image asset from git main branch**

Commands:
```bash
mkdir -p content/posts/technologies-i-am-investing-in-2024 content/posts/technologies-i-am-investing-in-2023 content/posts/neovim-lua content/posts/hello-hugo
git show main:content/posts/technologies-i-am-investing-in-2024/index.md > content/posts/technologies-i-am-investing-in-2024/index.md
git show main:content/posts/technologies-i-am-investing-in-2023/index.md > content/posts/technologies-i-am-investing-in-2023/index.md
git show main:content/posts/neovim-lua/index.md > content/posts/neovim-lua/index.md
git show main:content/posts/neovim-lua/preview-2.png > content/posts/neovim-lua/preview-2.png
git show main:content/posts/hello-hugo/index.md > content/posts/hello-hugo/index.md
```

- [ ] **Step 4: Run test to verify it passes**

Run: `bash tests/task1_articles_restore_test.sh`
Expected: PASS ("Task 1 files verified")

- [ ] **Step 5: Commit**

```bash
git add content/posts/ tests/task1_articles_restore_test.sh
git commit -m "feat: restore source markdown articles and assets in content/posts/"
```

---

### Task 2: Create Standalone Post Template (`templates/post.html`)

**Files:**
- Create: `templates/post.html`
- Test: `tests/task2_template_test.sh`

**Interfaces:**
- Consumes: CSS in `assets/css/`, JS in `assets/js/theme-toggle.js`, SVGs in `assets/favicons/favicon.svg`.
- Produces: Reusable template with substitution placeholders (`{{title}}`, `{{date}}`, `{{formatted_date}}`, `{{reading_time}}`, `{{tags_html}}`, `{{content}}`, `{{slug}}`).

- [ ] **Step 1: Write the test verifying template structure and placeholders**

Create `tests/task2_template_test.sh`:
```bash
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/task2_template_test.sh`
Expected: FAIL (missing `templates/post.html`)

- [ ] **Step 3: Implement `templates/post.html`**

Create `templates/post.html` with:
- Standard HTML5 boilerplate referencing relative assets (`../../assets/css/...`, `../../assets/favicons/favicon.svg`).
- Sticky Hunter HUD nav: `[← Terminal]` link to `../../#hunter-chronicles`, `@gcg` beacon, and theme toggle button.
- Manhwa container: `.webtoon-scroll` with `.system-window` wrapping the chronicle article.
- System header: `[SYSTEM ARCHIVE // CHRONICLE LOG]`, `{{title}}`, date badge, reading time, and tags.
- Body container: `.chronicle-prose` rendering `{{content}}`.
- Epilogue / Footer: "Hunter Chronicle Concluded", fedora badge, credit, and link back to home.
- Script inclusion: `../../assets/js/theme-toggle.js`.

- [ ] **Step 4: Run test to verify it passes**

Run: `bash tests/task2_template_test.sh`
Expected: PASS ("Task 2 template verified")

- [ ] **Step 5: Commit**

```bash
git add templates/post.html tests/task2_template_test.sh
git commit -m "feat: add standalone post template with solo leveling hud and theme toggle"
```

---

### Task 3: Implement Zero-Dependency Static Generator (`scripts/build_posts.py`)

**Files:**
- Create: `scripts/build_posts.py`
- Test: `tests/task3_build_posts_test.sh`

**Interfaces:**
- Consumes: Markdown files in `content/posts/`, template `templates/post.html`, homepage `index.html`.
- Produces: Generated HTML in `posts/<slug>/index.html`, copied media in `posts/<slug>/`, updated `index.html` chronicle cards.

- [ ] **Step 1: Write test for generator execution and output**

Create `tests/task3_build_posts_test.sh`:
```bash
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/task3_build_posts_test.sh`
Expected: FAIL (missing `scripts/build_posts.py`)

- [ ] **Step 3: Implement `scripts/build_posts.py`**

Features to implement in Python 3 standard library:
1. `parse_frontmatter(text)`: Extracts frontmatter between `---` fences into a dictionary (handles strings, lists, booleans, dates).
2. `markdown_to_html(md)`:
   - Escapes HTML entities inside fenced code blocks ` ```[lang] ... ``` ` -> `<pre><code class="language-[lang]">...</code></pre>`.
   - Converts headings `#` through `####` to `<h2>` through `<h5>` with slugified IDs.
   - Converts linked images `[![alt](img)](url)` and images `![alt](img)`.
   - Converts links `[text](url)` with `target="_blank" rel="noopener noreferrer"` for external URLs.
   - Converts unordered and ordered lists.
   - Converts blockquotes `>` to `<blockquote><p>...</p></blockquote>`.
   - Converts inline code `` `...` ``, `**bold**`, and `*italic*`.
   - Wraps paragraphs in `<p>...</p>`.
3. `format_date(iso_str)`: Formats ISO date to human readable (e.g. `February 1, 2024`).
4. `estimate_reading_time(text)`: Computes `~X min read` based on word count.
5. `build_posts()`:
   - Scans `content/posts/` for directories with `index.md` or `.md` files.
   - Skips files with `draft: true`.
   - Copies any sibling assets (e.g. `preview-2.png`) to `posts/<slug>/`.
   - Populates `templates/post.html` and writes `posts/<slug>/index.html`.
   - Generates sorted post list metadata for homepage synchronization.
6. `sync_homepage(posts_data)`:
   - Updates `index.html` between `<!-- CHRONICLES_START -->` and `<!-- CHRONICLES_END -->` markers with updated chronicle cards, ensuring titles and "Open Full Chronicle ↗" links target `/posts/<slug>/`.

- [ ] **Step 4: Run test to verify it passes**

Run: `bash tests/task3_build_posts_test.sh`
Expected: PASS ("Task 3 generator verified")

- [ ] **Step 5: Commit**

```bash
git add scripts/build_posts.py posts/ tests/task3_build_posts_test.sh
git commit -m "feat: implement zero-dependency python static article generator"
```

---

### Task 4: Integrate Homepage Sync Markers & Update Makefile

**Files:**
- Modify: `index.html:770-950`
- Modify: `Makefile:1-10`
- Test: `tests/task4_integration_test.sh`

**Interfaces:**
- Consumes: Output of `scripts/build_posts.py`.
- Produces: Delimited chronicle section in `index.html`, `make build` and `make serve` targets.

- [ ] **Step 1: Write test for Makefile and homepage integration**

Create `tests/task4_integration_test.sh`:
```bash
#!/bin/bash
set -e
grep -q "CHRONICLES_START" index.html || exit 1
grep -q "CHRONICLES_END" index.html || exit 1
grep -q "posts/technologies-i-am-investing-in-2024" index.html || exit 1
grep -q "Open Full Chronicle" index.html || exit 1
make build || exit 1
echo "Task 4 integration verified"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/task4_integration_test.sh`
Expected: FAIL (missing markers or make targets)

- [ ] **Step 3: Update `index.html` and `Makefile`**

1. In `index.html`, wrap the Chapter 04 chronicle list with `<!-- CHRONICLES_START -->` and `<!-- CHRONICLES_END -->`.
2. Ensure each chronicle card has:
   - Clickable title linking to `posts/<slug>/`.
   - "Preview Chronicle ▾" button for inline accordion preview.
   - "Open Full Chronicle ↗" link targeting `posts/<slug>/`.
3. In `Makefile`, add:
```makefile
.PHONY: all build serve clean

all: build serve

build:
	python3 scripts/build_posts.py

serve: build
	python3 -m http.server 8000
```
4. Run `python3 scripts/build_posts.py` to sync the homepage.

- [ ] **Step 4: Run test to verify it passes**

Run: `bash tests/task4_integration_test.sh`
Expected: PASS ("Task 4 integration verified")

- [ ] **Step 5: Commit**

```bash
git add index.html Makefile tests/task4_integration_test.sh
git commit -m "feat: integrate chronicle homepage sync markers and makefile build target"
```

---

### Task 5: End-to-End Verification & Test Suite

**Files:**
- Create: `tests/article_system_test.sh`
- Modify: existing test scripts if necessary to ensure all pass in combination.

**Interfaces:**
- Verifies: Full build pipeline, HTTP 200 responses for all article URLs, asset integrity, and theme switcher parity.

- [ ] **Step 1: Write comprehensive end-to-end test `tests/article_system_test.sh`**

Features to test:
1. `make build` runs cleanly.
2. All 4 article URLs exist and contain required tags, title, HUD nav, and theme switcher.
3. Neovim image `posts/neovim-lua/preview-2.png` is valid.
4. Homepage contains working links to all 4 articles.
5. Local server test: start server on port `8888`, send HTTP GET to `/posts/technologies-i-am-investing-in-2024/`, verify 200 OK. Send HTTP GET to `/posts/neovim-lua/preview-2.png`, verify 200 OK.
6. Verify dark and light mode tokens and classes exist on post pages.

- [ ] **Step 2: Run test to verify it passes**

Run: `bash tests/article_system_test.sh`
Expected: PASS ("Article system end-to-end verification passed!")

- [ ] **Step 3: Run full existing test suite to ensure no regressions**

Run:
```bash
bash tests/task1_verify.sh && bash tests/task2_css_verify.sh && node tests/task3_rotating_id_test.js && node tests/task4_hunter_fx_test.js && bash tests/task5_dom_verify.sh && bash tests/e2e_server_test.sh && bash tests/final_fix_pass_test.sh && bash tests/blog_and_theme_test.sh && bash tests/article_system_test.sh
```
Expected: All pass.

- [ ] **Step 4: Commit**

```bash
git add tests/article_system_test.sh
git commit -m "test: add comprehensive end-to-end test suite for standalone article system"
```
