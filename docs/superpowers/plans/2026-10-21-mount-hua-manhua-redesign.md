# Mount Hua Manhua Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild gcg.me as a full-colour Mount Hua murim-webtoon chapter.
- AI-painted scenes, with a code layer on top: lettering, talismans, sword qi, petals.
- Day and moonlit night themes.
- Self-hosted fonts.
- The blog restyled into the same world.

**Architecture:**
- **Static, no framework:** one `index.html` plus generated post pages.
- **Painted art:** raster images per scene and theme, two `<img>` per scene, with CSS showing the active one.
- **Overlays:** absolutely positioned inside scene panels. Each panel is a CSS container, so overlay sizes use `cqw` and scale with the art on any screen width.
- **Theme:** `data-theme` on `<html>`, set by an inline head snippet before first paint.
- **Blog:** `scripts/build_posts.py` keeps generating posts and refills the Scripture Pavilion list between the existing markers.

**Tech Stack:**
- Runtime: HTML, CSS, vanilla JS, Python 3 stdlib (build).
- One-off offline tools, never at build time:
  - Figma `generate_image` for the art.
  - `cwebp` (installed at `/opt/homebrew/bin/cwebp`) for image conversion.
  - fonttools + brotli for font subsetting. Install them in a scratch venv; the Homebrew `pyftsubset` is broken.

**Spec:** `docs/superpowers/specs/2026-10-21-mount-hua-manhua-redesign-design.md`

## Global Constraints

- **No new dependencies:** no npm, no frameworks, no bundler, no runtime or build dependencies. `make build` stays `python3 scripts/build_posts.py`.
- **Deploy:** the existing `.github/workflows/pages.yaml` uploads the repo root. Keep `CNAME`.
- **Fonts are self-hosted** from `assets/fonts/`. No request to fonts.googleapis.com or fonts.gstatic.com anywhere.
- **No photos of Guney anywhere.** Delete `assets/img/gcg.jpg`.
- **Prompts:** never name a specific series. Describe the style generically. Suns and moons are white or pale, never red.
- **Download immediately:** every Figma image link expires in 7 days. Download as soon as it's generated.
  - Keep the full-size PNG master in `.superpowers/redesign-assets/ai/` (gitignored).
  - Commit only the optimized WebP.
- **Figma credits:** use the "guney's team" plan (`team::1389603078137073604`) and file `zBgyhqtAIbuOi465lWdBka`. The cap is 150 credits a day, and every batch gets announced first.
- **Neon:** no neon UI boxes. Glow is allowed only on art effects (qi, petals, brush lettering).
- **Copy:** use the spec §4 verbatim. Cover tagline: "If you saw me fight, I didn't prepare enough." Title: 无名阵师 / "The Nameless Formation Master".
- **Chinese text:**
  - All Chinese gets `lang="zh"`.
  - Decorative Chinese (SFX, 封印, side rails) gets `aria-hidden="true"`.
  - Realm names get screen-reader English: 练气 Qi Refining, 筑基 Foundation Establishment, 金丹 Golden Core, 元婴 Nascent Soul.
- **Reduced motion:** `prefers-reduced-motion: reduce` stops petals, qi drawing and talisman sway.
- **Contrast:** text meets WCAG AA in both themes.
- **Theme storage:** `localStorage` key `theme-preference`, values `light` | `dark`, attribute `data-theme` on `<html>`.
- **Social links:**
  - https://github.com/gcg
  - https://twitter.com/gcg
  - https://instagram.com/gcg
  - https://phpc.social/@gcg (with `rel="me"`)
- **Other links:**
  - https://www.linkedin.com/in/guneycan
  - https://www.poltio.com
  - https://github.com/gcg/mdwriter
  - https://github.com/gcg/wpchanger

## Review Focus

1. **The visitor's own theme choice beats the OS setting.** Example: the toggle is set to dark while the OS is light. Night art and night colours must load with no flash of day on reload.
   - Pinned in Task 3, Step 5.
2. **Phone width (375px).** Overlays scale with the art: no lettering spills out of its panel, and the page has no horizontal scroll.
   - Pinned in Task 9, Step 2.
3. **Broken local paths:** fonts, art, CV, favicons, and post links, including `../../` paths from post pages.
   - Pinned by `test_local_links_resolve` (Task 8).
4. **Odd post metadata:**
   - a title containing `<` or `&`,
   - a post with no date,
   - a draft post,
   - running `make build` twice.

   The list must escape the title, show no year, skip the draft, and not duplicate rows.
   - Pinned in Task 2.
5. **JS disabled or failing.**
   - Every panel and link is still readable and usable.
   - The theme follows the OS through CSS alone.
   - Only the petals and the toggle button disappear.
   - Pinned in Task 9, Step 4.

---

## File Structure

| Path | Action | Responsibility |
|---|---|---|
| `assets/img/art/{cover,hero,cliff,backdrop}-{day,night}.webp` | create | painted scenes, optimized |
| `assets/fonts/*.woff2` | create | subset self-hosted fonts |
| `assets/css/fonts.css` | create | `@font-face` rules |
| `assets/css/variables.css` | rewrite | design tokens, day plus night overrides |
| `assets/css/style.css` | rewrite | page shell, backdrop, petals, strip, scene/text panels, lettering, post page |
| `assets/css/manhwa.css` | delete | old theme |
| `assets/js/theme-toggle.js` | modify | keep its API, restyle the button |
| `assets/js/petals.js` | create | generates the petal layers |
| `assets/js/main.js`, `hunter-fx.js`, `rotating-id.js` | delete | old effects |
| `assets/cv/Guney-Can-Gokoglu-CV.pdf` | create | CV, copied from `.superpowers/redesign-assets/` |
| `assets/img/gcg.jpg` | delete | photo, no longer used |
| `index.html` | rewrite | the 8-panel chapter |
| `templates/post.html` | rewrite | scripture-scroll post page |
| `scripts/build_posts.py` | modify | pavilion list renderer, lore strings |
| `scripts/subset_fonts.sh` | create | one-off font subsetting, re-run when Chinese text changes |
| `tests/test_build_posts.py` | create | generator unit tests |
| `tests/test_site.py` | create | link check and banned-vocabulary check |
| `tests/*` (old scripts) | delete | Gemini's old-markup tests |
| `Makefile` | modify | add a `test` target |
| `README.MD` | rewrite | short description, dev commands, art and font notes |

---

### Task 1: Paint the day scenes (main session; needs Guney's review)

**Files:**
- Create: `.superpowers/redesign-assets/ai/{hero,cliff,backdrop}-day.png` (masters, gitignored)
- Create: `assets/img/art/{cover,hero,cliff,backdrop}-day.webp`

**Interfaces:**
- Produces: four day WebPs at the paths above. Long edge ≤ 1600px. Cover, hero and cliff are at least 1200px wide. Quality 80.

- [ ] **Step 1: Announce the batch.** Tell Guney: "3 images (hero, cliff, backdrop, day)" before generating.
- [ ] **Step 2: Generate the hero.**
  - Call `generate_image` with `fileKey zBgyhqtAIbuOi465lWdBka`, model `gemini-3.1-flash-image`, at 1536×2048 (3:4 portrait).
  - Prompt: the Appendix A style sentence from the spec, plus the scene, plus the character block below.
  - **Scene:** "Blue hour on a snowy granite peak of Mount Hua; the figure stands on the summit rock in the lower-centre; needle spires and a sea of clouds below, lit pink from the right as if by a glowing sword; stars faint in a deep blue sky; leave calm sky in the upper right and upper left for lettering."
  - **Character block (use verbatim in the hero and cliff prompts):** "CHARACTER: a lone martial-arts cultivator seen strictly from behind, face never visible; black hair in a topknot tied with a long white ribbon; layered dark charcoal-grey robes with white trim; small pink plum-blossom motifs embroidered only in the corners of the garment (the hem corners, the sleeve cuffs and the collar tips), with no large emblem on the back and the back of the robe plain dark grey; a straight jian sword held lowered in the right hand."
  - End the prompt with: "No text, no letters, no logos, no watermark."
- [ ] **Step 3: Generate the cliff** at 2048×1536 (4:3). Same style sentence and character block.
  - **Scene:** "The cultivator sits on a black rock ledge with a snowy lip at the right of the frame, looking left over a misty Mount Hua range with a temple pavilion on a far summit; crisp winter morning, deep blue sky, white sun; a few pink plum petals drifting; the top-left is open blue sky, and the bottom-left corner is natural dark granite rock in the foreground." Add to every prompt: "one single continuous image … no boxes, no frames, no panel borders, no inset panels" (asking for a caption area makes the model draw a box).
- [ ] **Step 4: Generate the backdrop** at 2048×1152 (16:9). Same style sentence, **no character**.
  - **Scene:** "Wide panoramic Mount Hua range in winter: granite needle spires with snow on ledges and pines, a sea of clouds, a pavilion on one summit, a black pine treeline along the bottom and white snow; soft and slightly hazy so it can sit behind content; the centre third is calmer and lighter; no plum branch."
- [ ] **Step 5: Download each image.** Run `curl -fL -o .superpowers/redesign-assets/ai/<scene>-day.png "<image.url>"` right after each generation.
- [ ] **Step 6: Check consistency.** View the hero and cliff side by side (Read tool). The hair, ribbon, robe colours and emblem must match.
  - If they don't, regenerate the weaker one, at most 2 retries each.
  - Retries count against the 150/day cap. If the cap is hit, stop and resume tomorrow.
- [ ] **Step 7: Convert to WebP.** For each scene, including the existing `cover-day.png`:
  ```bash
  cwebp -q 80 -resize <w> 0 <master>.png -o assets/img/art/<scene>-day.webp
  ```
  Use `<w>` = 1200 for cover, hero and cliff, and 1600 for the backdrop.
  - Expected: four files, each under 350 KB, backdrop under 400 KB.
- [ ] **Step 8: Guney review.** Show the four day images in the companion or in Read. Wait for approval before Task 3. Regenerate whatever Guney rejects.
- [ ] **Step 9: Commit**
  ```bash
  git add assets/img/art/*-day.webp
  git commit -m "art: add painted day scenes for cover, hero, cliff, backdrop"
  ```

### Task 2: Pavilion list renderer in the post generator (TDD)

**Files:**
- Modify: `scripts/build_posts.py`
  - `extract_excerpt` fallback string (line ~106)
  - replace `sync_homepage` (lines ~366–434)
  - module docstring (lines 2–6)
- Create: `tests/test_build_posts.py`

**Interfaces:**
- Consumes: the existing post dicts from `build_posts()`, with keys `slug`, `title`, `date`, `formatted_date`, `excerpt`, `tags`, `tags_html`, `body_html`, `reading_time`.
- Produces:
  - `post_year(date_raw) -> str`: `"2024"` from `"2024-02-01T14:33:01+03:00"`; `""` for missing or garbage input.
  - `render_pavilion(posts: list[dict]) -> str`: one `<li class="scroll-row"><a href="posts/{slug}/">{escaped title}</a><span class="scroll-year">{year}</span></li>` per post, in the given order, joined by `"\n"`.
  - `sync_homepage(posts: list[dict], homepage_path: str = HOMEPAGE_PATH) -> bool`:
    - Replaces everything between `<!-- CHRONICLES_START -->` and `<!-- CHRONICLES_END -->` with `render_pavilion(posts)` and returns `True`.
    - Returns `False` and leaves the file untouched if either marker is missing.
  - In `index.html` (Task 5) the markers sit inside `<ol class="scrolls">`.

- [ ] **Step 1: Write failing tests** in `tests/test_build_posts.py`.
  - Use `unittest`, and import the module via `importlib.util.spec_from_file_location("build_posts", "scripts/build_posts.py")`.
  - **`test_post_year`:**
    - `post_year("2024-02-01T14:33:01+03:00") == "2024"`
    - `post_year("") == ""`
    - `post_year(None) == ""`
    - `post_year("soon") == ""`
  - **`test_render_pavilion_escapes_and_orders`:**
    - Input: posts `[{"slug":"b","title":"Vim & <Lua>","date":"2024-01-01"},{"slug":"a","title":"Hello","date":""}]`.
    - Output contains `<a href="posts/b/">Vim &amp; &lt;Lua&gt;</a><span class="scroll-year">2024</span>`.
    - Output contains `<a href="posts/a/">Hello</a><span class="scroll-year"></span>`.
    - The `posts/b/` row comes before `posts/a/`.
  - **`test_sync_homepage_is_idempotent`:**
    - Set up a temp file `"<ol class=\"scrolls\"><!-- CHRONICLES_START -->old<!-- CHRONICLES_END --></ol>"`.
    - Sync twice with the same 2 posts.
    - The file has exactly 2 `scroll-row` occurrences, and `old` is gone.
    - Both calls return `True`.
  - **`test_sync_homepage_without_markers`:** a temp file without markers. Returns `False` and the content is unchanged.
  - **`test_build_skips_drafts_and_sorts_newest_first`:**
    - Run `python3 scripts/build_posts.py` with `subprocess`; exit code 0.
    - Read `index.html` between the markers.
    - Slugs appear in this order: `technologies-i-am-investing-in-2024`, `technologies-i-am-investing-in-2023`, then `neovim-lua` and `hello-hugo`.
    - Each `posts/<slug>/index.html` exists.
    - This test needs Task 5's markers; mark it `@unittest.skipUnless('class="scrolls"' in index_html, ...)` until then.
- [ ] **Step 2: Run the tests.** `python3 -m unittest tests/test_build_posts.py -v`. Expected: FAIL, with `AttributeError` on `post_year` / `render_pavilion`.
- [ ] **Step 3: Implement.**
  - Add `post_year` and `render_pavilion` to `scripts/build_posts.py`, and rewrite `sync_homepage` to the signature above, using `html.escape` on titles.
  - Change `extract_excerpt`'s fallback to `"A scroll from the Scripture Pavilion of gcg.me."`
  - Change the docstring and print lines to say "Scripture Pavilion" instead of "Chapter 04 chronicle cards".
- [ ] **Step 4: Run the tests.** Same command. Expected: 4 passed, 1 skipped.
- [ ] **Step 5: Commit**
  ```bash
  git add scripts/build_posts.py tests/test_build_posts.py
  git commit -m "feat(blog): render Scripture Pavilion rows; drop chronicle cards"
  ```

### Task 3: Page shell, design tokens, theme, backdrop, petals

**Files:**
- Rewrite: `assets/css/variables.css`
- Rewrite: `assets/css/style.css`. This task adds the shell section only; later tasks append sections.
- Modify: `assets/js/theme-toggle.js`
- Create: `assets/js/petals.js`
- Rewrite: `index.html`. This task adds the shell only: head, backdrop, petal layers, an empty `<main class="strip">`, and the toggle.

**Interfaces:**
- **Tokens** (in `variables.css`, on `:root`, with night overrides):
  - `--paper`, `--ink`, `--ink-border`, `--accent`, `--plum`, `--plum-2`, `--plum-3`, `--bud`, `--qi`, `--qi-core`, `--narr-bg`, `--narr-rule`, `--page-top`, `--page-bottom`.
  - Day and night values come from spec §3.5.
  - Night overrides go under `:root[data-theme="dark"]`, and also under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }`.
- **Image swap classes:**
  - `.art--day` is visible by default; `.art--night` is `display:none`.
  - Swapped by the same two night selectors.
  - Imgs get `loading="lazy"` and `decoding="async"`. The only exception is the cover's day img, which gets `fetchpriority="high"` and no lazy.
- **Shell DOM:**
  - `<div class="backdrop" aria-hidden="true">`, holding `img.art.art--day` / `img.art.art--night`, both `backdrop-*.webp`.
  - `<div id="petals-back" class="petals" aria-hidden="true">` and `<div id="petals-front" class="petals petals--front" aria-hidden="true">`.
  - `<button id="theme-toggle-btn" class="theme-toggle" type="button">`, fixed at the top-left, 40px round, on ink paper.
  - `<main class="strip">`, a centred column with `max-width: 600px`, 40px gap between children, and 16px side padding on phones.
  - `<aside class="side-rail" aria-hidden="true" lang="zh">华山 · 无名阵师</aside>`, shown only at ≥ 1100px.
- **JS:**
  - `theme-toggle.js` keeps its exports: `getSystemTheme`, `getStoredTheme`, `applyTheme`, `toggleTheme`, `initTheme`, and `STORAGE_KEY 'theme-preference'`. Remove the "Solo Leveling" comment.
  - `petals.js` exposes `initPetals(container: HTMLElement, count: number, opts: {front: boolean})`. It creates `count` `<i>` elements with CSS custom properties `--x --d --dl --dx --s --c --o --b`. It auto-runs on `DOMContentLoaded` with 60 behind and 6 in front.

- [ ] **Step 1: Inline no-flash snippet.** Put it in `<head>` before any stylesheet:
  ```html
  <script>try{var t=localStorage.getItem('theme-preference');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>
  ```
  Stylesheet order: `fonts.css` (created in Task 7; link it now), `reset.css`, `variables.css`, `style.css`. Scripts are `theme-toggle.js` and `petals.js` with `defer`. Keep the existing favicon links verbatim.
- [ ] **Step 2: Write the shell CSS.**
  - **Backdrop:** `position: fixed; inset: 0; z-index: 0`. The img uses `object-fit: cover`. A gradient overlay fades from transparent into `var(--page-bottom)` over the bottom 35% and the side edges.
  - **Body:** gradient `var(--page-top)` → `var(--page-bottom)`.
  - **Petals:** port the falling keyframes and 3D flutter from mockup `hua-v5b.html`. Behind petals use z-index 0; front petals use z-index 3 with `filter: blur(var(--b))`.
  - **Reduced motion:** `@media (prefers-reduced-motion: reduce) { .petals { display: none } }`.
- [ ] **Step 3: Implement `petals.js`.** Pink petals use `--plum`, `--plum-2` and `--plum-3`; about 30% of the behind petals are white snowflakes.
- [ ] **Step 4: Check it renders.** Run `make serve`, open http://localhost:8000.
  - Expected: the backdrop fills the viewport, petals fall, and the toggle switches the backdrop between day and night.
  - The night WebP doesn't exist yet. Its absence is expected until Task 9; the day art must show.
- [ ] **Step 5: Pin Review Focus #1.** In the browser, run `localStorage.setItem('theme-preference','dark')` with the OS in light mode, then reload.
  - `getComputedStyle(document.documentElement).getPropertyValue('--paper').trim()` must be `#101826`.
  - `document.querySelector('.backdrop .art--night')` must have computed `display` other than `none`.
  - Clear the key afterwards.
- [ ] **Step 6: Commit**
  ```bash
  git add index.html assets/css/variables.css assets/css/style.css assets/js/theme-toggle.js assets/js/petals.js
  git commit -m "feat: page shell with day/night tokens, painted backdrop, petals, no-flash theme"
  ```

### Task 4: Scene panels: cover, hero, cliff

**Files:**
- Modify: `index.html`, adding three `section.scene` elements inside `main.strip`
- Modify: `assets/css/style.css`, appending the "scene panels and lettering" section

**Interfaces:**
- Consumes:
  - the Task 1 art paths,
  - the Task 3 classes `.art--day` / `.art--night` and the tokens.
- Produces these classes, reused in Tasks 5 and 6:
  - `.scene`: `position: relative; container-type: inline-size; aspect-ratio` set per panel from the art's real ratio.
  - `.scene > img.art`: `position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover`.
  - `.narr`: narration box.
  - `.sfx`: huge brush SFX.
  - `.brush`: big brush lettering with white or gradient fill, `-webkit-text-stroke` in `--ink`, `paint-order: stroke fill`, and a `--plum` glow.
  - `.technique`: brush name, Cinzel subtitle, and a `code` chip.
  - `.talismans` with `a.talisman` children.
  - `.label`: small letter-spaced uppercase in `--accent`.
- **Overlay sizing rule:**
  - Positions are in `%` of the panel.
  - Font sizes and paddings in overlays are in `cqw`, so the composition scales like the image.
  - Starting values from spike `spike-murim-v2.html` at 600px: title 78px → `13cqw`, name 38px → `6.3cqw`, narration 17px → `2.9cqw`, SFX 120px → `20cqw`.
  - Clamp any `cqw` text with a minimum of 12px for legibility.

- [ ] **Step 1: Cover markup** (`section.scene.scene--cover`, `aria-labelledby` pointing at the h1).
  - Two imgs for the art, with `alt=""`.
  - Four `a.talisman` links (vertical text "github @gcg" etc., `@gcg` in `<b>`), with Mastodon `rel="me"`.
  - `<div class="brush brush--title" lang="zh">无名阵师</div>`. Give it screen-reader English through a visually hidden span: "The Nameless Formation Master".
  - Lower left, over the dark trees:
    - `.label` "The Nameless Formation Master"
    - `<h1>Guney Can Gokoglu</h1>`
    - tagline `<p>`: "If you saw me fight, I didn't prepare enough."
  - Talismans sway with a 4s alternate animation, off under reduced motion.
- [ ] **Step 2: Hero markup** (`section.scene.scene--hero`).
  - Two imgs with `alt="A cultivator seen from behind on a snowy Mount Hua peak, sword lowered, plum blossoms bursting"`.
  - Inline `<svg class="qi" aria-hidden="true" viewBox matching the art>`. It holds 7–9 glowing arcs (`path.qa`, gradient `--qi` → `--qi-core` → transparent, Gaussian bloom filter) and 15–25 blossoms, centred on the sword tip in the painting. Read the tip position off the actual art.
  - The arcs animate `stroke-dashoffset` from full to 0 over 2.4s, staggered. Under reduced motion they render fully drawn.
  - `.narr`: "Tallinn, in winter. Twenty-five years since the first install."
  - `.sfx` `唰!!`, with `aria-hidden`.
  - `.technique`:
    - `梅花剑法` (`lang="zh"`)
    - "Plum Blossom Sword Art · Form 25"
    - `<code>$ sudo dnf upgrade --refresh</code>`
  - Place the text in the calm sky areas the painting left.
- [ ] **Step 3: Cliff markup** (`section.scene.scene--cliff`), placed after the arc-title panel slot. Task 5 inserts the arc title before it.
  - Two imgs with `alt="The same cultivator seated on a cliff ledge, looking over a misty Mount Hua range"`.
  - Top-left `.narr`: "Twelve years ago, a sect was founded."
  - Bottom-left `.narr`: "Some build a sect to be remembered. Others build one that simply never falls."
- [ ] **Step 4: Check placement.** With `make serve`, check at 1280px and at 375px (browser pane `resize_window` with `width:375,height:812`).
  - At both widths, no overlay text crosses a busy part of the painting so badly that it's illegible.
  - Nothing overflows its panel.
  - Adjust the `%` positions and `cqw` sizes until both pass.
- [ ] **Step 5: Commit**
  ```bash
  git add index.html assets/css/style.css
  git commit -m "feat: cover, hero and cliff scene panels with lettering and sword qi"
  ```

### Task 5: Text panels: registry, arc title, creed, treasures, pavilion, ending

**Files:**
- Modify: `index.html`, adding text panels in spec §4 order
- Modify: `assets/css/style.css`, appending the "text panels" section

**Interfaces:**
- Consumes:
  - the Task 4 classes `.label` and `.brush`, and the tokens,
  - the Task 2 contract: `<ol class="scrolls"><!-- CHRONICLES_START --> … <!-- CHRONICLES_END --></ol>`.
- Produces:
  - `.panel`: an ink-and-paper text panel. 3px solid `var(--ink-border)`, `border-radius: 3px 7px 4px 6px`, background `var(--paper)`, colour `var(--ink)`, and an offset shadow.
  - The `scrolls` list markup used by the generator.

- [ ] **Step 1: Sect registry** (`section.panel.registry`), after the hero.
  - Copy the structure and rows from spec §4 Panel 3. Port the layout from mockup `hua-v6.html` `.reg`, with the seal removed.
  - The realm climb is an inline SVG ported from `hua-v6.html` `.realm-svg`.
    - Each Chinese realm name gets `lang="zh"` plus a `<title>` or visually hidden English name.
    - At night, its colours come from the tokens, not hard-coded hex.
- [ ] **Step 2: Arc title** (`section.panel.arc`), between the registry and the cliff.
  - `.label` "Main arc · 2014 — now"
  - `.brush` `第二卷 · 立宗`
  - "The Poltio Sect: Twelve Years"
  - an `<a href="https://www.poltio.com">poltio.com</a>`
- [ ] **Step 3: Creed** (`section.panel.creed`), after the cliff. Copy the text verbatim from spec §4 Panel 5, with vertical brush text on the left.
- [ ] **Step 4: Treasure Pavilion** (`section.panel.treasures`). A 2×2 grid, one column under 420px.
  - mdwriter and wpchanger are cards linking to their repos.
  - Two sealed cards with an `aria-hidden` 封印 talisman and the visible text "Sealed · opening soon".
- [ ] **Step 5: Scripture Pavilion** (`section.panel.pavilion`, `id="scripture-pavilion"`).
  - `.label` "藏经阁 · Scripture Pavilion · Blog", with 藏经阁 in `lang="zh"`.
  - `<ol class="scrolls">` with the two markers inside it.
  - Style `.scroll-row` as in mockup `.scroll`: title left, year right in muted italic, rule lines between rows.
- [ ] **Step 6: Ending** (`footer.panel.end`).
  - `<p lang="zh" class="brush">未完待续</p>`
  - *To be continued…*
  - `<a href="assets/cv/Guney-Can-Gokoglu-CV.pdf">Read the full sect records (CV) ↗</a>`
  - a small LinkedIn link
  - Copy the CV: `cp .superpowers/redesign-assets/Guney-Can-Gokoglu-CV.pdf assets/cv/`
- [ ] **Step 7: Build and test.**
  - Run `make build`. Expected output includes "Successfully processed 4 articles", and 4 `scroll-row` items appear in `index.html`.
  - Run `python3 -m unittest tests/test_build_posts.py -v`. Expected: 5 passed, now including the build test.
- [ ] **Step 8: Commit**
  ```bash
  git add index.html assets/css/style.css assets/cv/Guney-Can-Gokoglu-CV.pdf
  git commit -m "feat: registry, Poltio arc, creed, treasures, Scripture Pavilion and ending panels"
  ```

### Task 6: Post page template

**Files:**
- Rewrite: `templates/post.html`
- Modify: `assets/css/style.css`, appending the "post page" section

**Interfaces:**
- Consumes:
  - The template placeholders filled by `build_posts.py`, unchanged: `{{title}} {{slug}} {{formatted_date}} {{date}} {{reading_time}} {{excerpt}} {{tags_html}} {{content}}`.
  - The Task 3 shell: no-flash snippet, backdrop, petals, toggle, and asset paths prefixed `../../`.
- Produces: `article.panel.scroll-page` with header `.label` `{{formatted_date}} · {{reading_time}}`, `<h1>{{title}}</h1>`, and `{{tags_html}}`.
  - Then `div.prose` with `{{content}}`.
  - Then a back link `<a href="../../#scripture-pavilion">← Back to the Scripture Pavilion</a>`.

- [ ] **Step 1: Write the template.** Same `<head>` as `index.html`, with paths prefixed `../../` and `<title>{{title}} — Guney Can Gokoglu (@gcg)</title>`.
  - The body has the shell plus `main.strip` holding a narrow cover strip (a `.scene` 600:180 crop of `cover-{day,night}.webp`, `object-position: top`) with a link home ("← gcg.me").
  - Then the article.
- [ ] **Step 2: Prose styles.**
  - Text in Cormorant Garamond, at least 19px.
  - `.tag-pill` as small ink chips.
  - Code blocks: `pre` in JetBrains Mono on `#0b1030` with light text in both themes, and an inline `code` chip.
  - Images at `max-width: 100%`.
- [ ] **Step 3: Rebuild and look.** Run `make build`, open `/posts/neovim-lua/`.
  - The `preview-2.png` image shows.
  - Code blocks are readable in day and night.
  - The back link lands on the pavilion.
- [ ] **Step 4: Commit**
  ```bash
  git add templates/post.html assets/css/style.css posts/
  git commit -m "feat(blog): scripture-scroll post template"
  ```

### Task 7: Self-hosted subset fonts

**Files:**
- Create: `scripts/subset_fonts.sh`
- Create: `assets/fonts/{ma-shan-zheng,cinzel,cormorant-garamond,cormorant-garamond-italic,shantell-sans,jetbrains-mono}.woff2`
- Create: `assets/css/fonts.css`

**Interfaces:**
- Produces the font families used by `style.css`: `'Ma Shan Zheng'`, `'Cinzel'`, `'Cormorant Garamond'` (normal and italic), `'Shantell Sans'`, `'JetBrains Mono'`. All use `font-display: swap`.

- [ ] **Step 1: Get the sources.**
  - Download the OFL TTFs from https://github.com/google/fonts, under `ofl/mashanzheng`, `ofl/cinzel`, `ofl/cormorantgaramond`, `ofl/shantellsans` and `ofl/jetbrainsmono`.
  - Save them to `.superpowers/redesign-assets/fonts-src/` (gitignored).
  - Install the tools in a scratch venv: `python3 -m venv <scratch>/venv && <scratch>/venv/bin/pip install fonttools brotli`.
- [ ] **Step 2: Write `scripts/subset_fonts.sh`.** Header comment: "one-off; re-run after adding Chinese text; needs fonttools+brotli (FONTTOOLS=path/to/pyftsubset)".
  - It collects every CJK character (U+3000–U+9FFF, U+FF00–U+FFEF) from `index.html` and `templates/post.html` with `python3 -c`.
  - It runs `pyftsubset` for Ma Shan Zheng with `--text=<chars>!?·` and `--flavor=woff2`.
  - Latin fonts use `--unicodes=U+0000-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2190-2193,U+20AC` and `--flavor=woff2`. This range includes the `→ ← ↗ · — …` characters the copy uses.
  - Variable axes are kept.
- [ ] **Step 3: Run it.** Expected: `ma-shan-zheng.woff2` under 60 KB, and every file under 120 KB.
- [ ] **Step 4: Write `assets/css/fonts.css`** with one `@font-face` per file (weight ranges for the variable fonts). Remove any Google Fonts `@import` or `<link>`.
- [ ] **Step 5: Verify.** Run `grep -rn "fonts.googleapis\|fonts.gstatic" index.html templates assets` and expect no matches.
  - In the browser, `document.fonts.check('40px "Ma Shan Zheng"', '无名阵师')` must be `true` after load, on the homepage and on a post page.
- [ ] **Step 6: Commit**
  ```bash
  git add scripts/subset_fonts.sh assets/fonts assets/css/fonts.css
  git commit -m "feat: self-host subset fonts"
  ```

### Task 8: Remove the old site, add site-level checks

**Files:**
- Delete:
  - `assets/css/manhwa.css`
  - `assets/js/main.js`, `assets/js/hunter-fx.js`, `assets/js/rotating-id.js`
  - `assets/img/gcg.jpg`
  - every old file in `tests/` (the `.sh` and `.js` scripts)
- Create: `tests/test_site.py`
- Modify: `Makefile`, `README.MD`

**Interfaces:**
- Produces: `make test` runs `python3 -m unittest discover -s tests -v`.

- [ ] **Step 1: Write `tests/test_site.py`** (stdlib `unittest` and `html.parser`).
  - **`test_local_links_resolve`:**
    - For `index.html` and every `posts/*/index.html`, collect `href`/`src` values that aren't `http(s):`, `mailto:` or `#…`.
    - Strip any `#fragment`.
    - Resolve each relative to the file's directory; a trailing `/` means `index.html`.
    - Assert every target exists.
    - The failure message lists the missing paths.
  - **`test_no_solo_leveling_vocabulary`:**
    - In `index.html`, `templates/post.html`, `scripts/build_posts.py`, `assets/css/*.css`, `assets/js/*.js` and `posts/*/index.html`:
    - none of `Hunter`, `hunter`, `Solo Leveling`, `system-window`, `Monarch`, `Chronicle Log`, `fonts.googleapis` may appear.
  - **`test_reduced_motion_rules_exist`:**
    - `assets/css/style.css` contains a `prefers-reduced-motion: reduce` block.
    - That block mentions `.petals`, `.qa` and `.talisman`.
- [ ] **Step 2: Delete the old files.** Run `make build`, then `make test`.
  - Expected: all tests pass (5 in `test_build_posts`, 3 in `test_site`).
  - If `test_local_links_resolve` fails, fix the path, not the test.
- [ ] **Step 3: Update the Makefile and README.**
  - Makefile: add `.PHONY: test` and a target `test: build` that runs `python3 -m unittest discover -s tests -v`.
  - Remove "Solo Leveling" from the `serve` echo.
  - README.MD:
    - a one-paragraph description,
    - `make` / `make test`,
    - "Art: painted with Figma AI; prompts and masters in `.superpowers/redesign-assets` (local); see the spec Appendix A",
    - "Fonts: re-run `scripts/subset_fonts.sh` after adding Chinese text".
- [ ] **Step 4: Commit**
  ```bash
  git add -A assets tests Makefile README.MD
  git commit -m "chore: remove Solo Leveling site, add site checks and make test"
  ```

### Task 9: Night art and the final pass (main session; needs Guney's review)

**Files:**
- Create: `.superpowers/redesign-assets/ai/{cover,hero,cliff,backdrop}-night.png`
- Create: `assets/img/art/{cover,hero,cliff,backdrop}-night.webp`
- Modify: `index.html` / `assets/css/style.css`, but only for per-theme overlay nudges

**Interfaces:**
- Consumes: the Task 1 prompts and the Task 4 overlay layout.
- Produces: the night art at the same paths and sizes as day.

- [ ] **Step 1: Announce and generate.** Tell Guney: "4 images (night)".
  - Re-use each day prompt.
  - Replace the light description with: "Night under a pale full moon (white, never red) and stars; deep Estonian-blue sky; snow glowing in moonlight; plum blossoms catching the light; same composition and calm areas as described."
  - Download immediately, then convert with the same `cwebp` command as Task 1, Step 7.
  - If a night painting's calm areas differ from day, nudge overlay positions under the night selectors only.
- [ ] **Step 2: Pin Review Focus #2.** Check at 375×812 in both themes:
  - `document.documentElement.scrollWidth <= window.innerWidth` is `true`.
  - Every element inside `.scene` has `getBoundingClientRect()` inside its panel's rect.
- [ ] **Step 3: Full check in both themes at 1280 and 375:**
  - every panel in spec §4 order,
  - the talismans open the four profiles,
  - the CV opens,
  - the pavilion links open posts, and their back links return,
  - the toggle persists across reload and across navigation into a post.
- [ ] **Step 4: Pin Review Focus #5.** Disable JS (browser devtools, or load with `?` after temporarily removing the two `<script>` tags locally, then restoring them).
  - All panels and links still work.
  - The theme follows the OS through the `prefers-color-scheme` selectors.
- [ ] **Step 5: Run the checks.** `make test`. Expected: all pass.
- [ ] **Step 6: Guney review.** Ask Guney to review in the browser in both themes, and adjust anything rejected.
- [ ] **Step 7: Commit**
  ```bash
  git add assets/img/art/*-night.webp index.html assets/css/style.css
  git commit -m "art: add moonlit night scenes and final layout pass"
  ```
