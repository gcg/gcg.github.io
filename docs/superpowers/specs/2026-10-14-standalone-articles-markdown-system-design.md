# Design Spec: Standalone Blog Articles & Zero-Dependency Markdown System

## 1. Overview
This specification defines the architecture, data flow, generator script, and page templates for turning the "Hunter Chronicles" section of `gcg.github.io` (`gcg.me`) into a standalone article publishing system with dedicated URLs, while retaining the Solo Leveling / Action Manhwa "System Window" aesthetic.

## 2. Goals & Success Criteria
1. **Dedicated Article URLs**: Each blog post is served at its own canonical URL under `/posts/<slug>/` (resolving to `/posts/<slug>/index.html`), preserving historical Hugo URLs.
2. **Authoring Simplicity**: New articles can be added simply by dropping a Markdown file into `content/posts/<slug>/index.md` (or `<slug>.md`) with YAML frontmatter.
3. **Zero Dependencies**: The markdown-to-HTML generator is written in pure Python 3 using only the standard library (`urllib`, `re`, `shutil`, `datetime`, `html`, `pathlib`). No `pip install` or external build tools are required.
4. **Automated Homepage Sync**: Running `make build` (or `python3 scripts/build_posts.py`) generates all post pages and synchronizes the Chapter 04 chronicle list on the homepage `index.html`.
5. **Aesthetic & Theme Parity**: Standalone article pages feature the complete Solo Leveling theme, top HUD with `← Return to Hunter Terminal`, `@gcg` rotating beacon, dark/light mode toggle with full background coverage, and responsive layouts.
6. **Local Development Integration**: `Makefile` includes `make build` and ensures `make` / `make serve` builds the articles before serving on `http://localhost:8000`.

## 3. Directory Layout
```
.
├── content/
│   └── posts/
│       ├── technologies-i-am-investing-in-2024/
│       │   └── index.md
│       ├── technologies-i-am-investing-in-2023/
│       │   └── index.md
│       ├── neovim-lua/
│       │   ├── index.md
│       │   └── preview-2.png
│       └── hello-hugo/
│           └── index.md
├── templates/
│   └── post.html           # Standalone article template with Solo Leveling HUD & theme
├── scripts/
│   └── build_posts.py      # Zero-dependency Python 3 static builder
├── posts/                  # Generated output directory (committed for GitHub Pages)
│   ├── technologies-i-am-investing-in-2024/
│   │   └── index.html
│   ├── technologies-i-am-investing-in-2023/
│   │   └── index.html
│   ├── neovim-lua/
│   │   ├── index.html
│   │   └── preview-2.png
│   └── hello-hugo/
│       └── index.html
├── index.html              # Homepage (Chapter 04 cards link to /posts/<slug>/)
└── Makefile                # Includes build target and serve dependency
```

## 4. Markdown Specification & Parsing
The generator in `scripts/build_posts.py` handles:
1. **YAML Frontmatter**:
   - `title`: String (e.g. `"Technologies I Am Investing in 2024"`).
   - `date`: ISO timestamp or date string (e.g. `2024-02-01T14:33:01+03:00`).
   - `tags`: Array of strings or comma-separated list.
   - `draft`: Boolean (if `true`, excluded from production builds).
2. **Markdown Syntax Support**:
   - **Headings**: `#` to `####` mapped to `<h2>` to `<h5>` inside article body with generated slug IDs for bookmarking.
   - **Code Blocks**: Fenced blocks ` ```[lang] ... ``` ` converted to `<pre><code class="language-[lang]">...</code></pre>` with HTML entities escaped (`&`, `<`, `>`).
   - **Inline Code**: `` `code` `` converted to `<code>code</code>`.
   - **Links**: `[text](url)` converted to `<a href="url" target="_blank" rel="noopener noreferrer">text</a>` (external) or relative links (internal).
   - **Images & Linked Images**:
     - `![alt](src)` -> `<figure><img src="src" alt="alt" loading="lazy"><figcaption>alt</figcaption></figure>`.
     - `[![alt](src)](url)` -> `<a href="url" target="_blank" rel="noopener noreferrer"><img src="src" alt="alt" loading="lazy"></a>`.
   - **Lists**: Unordered (`-`, `*`) and ordered (`1.`) with proper nesting into `<ul><li>` and `<ol><li>`.
   - **Blockquotes**: `> text` converted to `<blockquote><p>text</p></blockquote>`.
   - **Paragraphs & Formatting**: Double newline creates `<p>...</p>`, `**bold**`, `*italic*`.

## 5. Standalone Post Template (`templates/post.html`)
The template includes:
1. **HTML Shell & Assets**:
   - Viewport and charset meta tags.
   - Favicons referencing `../../assets/favicons/favicon.svg`.
   - CSS: `../../assets/css/reset.css`, `../../assets/css/variables.css`, `../../assets/css/manhwa.css`, `../../assets/css/style.css`.
2. **Hunter Navigation HUD**:
   - Back Link: `<a href="../../#hunter-chronicles" class="hud-back-btn">← Terminal</a>`.
   - Rotating Beacon: `@gcg` identity badge with flip animation and active links.
   - Theme Toggle: Moon/Sun SVG button bound to `../../assets/js/theme-toggle.js`.
3. **Chronicle Header**:
   - System Notice: `[SYSTEM ARCHIVE // CHRONICLE LOG]`.
   - Title: `{{title}}`.
   - Metadata Row: Formatted Date (`{{formatted_date}}`), reading time estimate (`{{reading_time}}`), and tag pills (`{{tags_html}}`).
4. **Article Body**:
   - Wrapped in `.system-window` and `.chronicle-prose`.
   - Dynamic content injection: `{{content}}`.
5. **Epilogue / Footer**:
   - Return to hunter terminal button.
   - Fedora badge and copyright text.

## 6. Homepage Synchronization (`index.html`)
In `index.html`, Chapter 04 ("Hunter Chronicles & Archives") contains a sync delimiter:
```html
<!-- CHRONICLES_START -->
... dynamic list of chronicle cards ...
<!-- CHRONICLES_END -->
```
Each card contains:
- Title linking directly to `/posts/<slug>/`.
- Date and tags.
- Excerpt from the article.
- Actions row:
  - `Preview Chronicle ▾`: Toggles the inline accordion preview.
  - `Open Full Chronicle ↗`: Anchor pointing directly to `/posts/<slug>/`.

## 7. Makefile Updates
```makefile
.PHONY: all build serve clean

all: build serve

build:
	python3 scripts/build_posts.py

serve: build
	python3 -m http.server 8000
```

## 8. Error Handling & Edge Cases
- **Missing Frontmatter Fields**: If `title` is missing, defaults to directory slug; if `date` is missing, defaults to file modification time.
- **Drafts**: Files with `draft: true` are logged and skipped.
- **Relative Asset Copying**: Any non-markdown asset located inside `content/posts/<slug>/` is copied directly to `posts/<slug>/`.
- **Character Encoding**: Enforces UTF-8 reading and writing across all files.

## 9. Testing & Verification
A test script `tests/article_system_test.sh` verifies:
1. `python3 scripts/build_posts.py` runs with exit code 0.
2. Output HTML files exist in `posts/<slug>/index.html` for all 4 articles:
   - `technologies-i-am-investing-in-2024`
   - `technologies-i-am-investing-in-2023`
   - `neovim-lua`
   - `hello-hugo`
3. Asset `posts/neovim-lua/preview-2.png` exists and is non-empty.
4. Each generated HTML file contains the Hunter HUD navigation, theme toggle script, and `<article>` content.
5. `index.html` links to `/posts/<slug>/`.
6. An HTTP server test verifies `/posts/technologies-i-am-investing-in-2024/` returns HTTP 200 with appropriate Content-Type.
