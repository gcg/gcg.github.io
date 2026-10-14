# Solo Leveling Webtoon Personal Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bespoke, single-page personal website for Guney Can Gokoglu (@gcg) inspired by a Solo Leveling / Action Manhwa "System Window" webtoon, completely replacing the legacy Hugo site with zero-dependency vanilla HTML5, CSS3, and modern JavaScript.

**Architecture:** A lightweight static site organized around a vertical webtoon reading experience. Modular CSS (reset, theme variables, manhwa components, layout) and focused vanilla JavaScript modules (rotating `@gcg` social beacon, scroll observers, dynamic counters, holographic scanline effects) served via a simple Python-backed Makefile runner.

**Tech Stack:** Semantic HTML5, Modern CSS3 (Grid, Flexbox, Custom Properties, Keyframe Animations, Glassmorphism), Vanilla JavaScript (ES6+, IntersectionObserver API), Python 3 (`http.server` for local development).

**Spec:** [docs/superpowers/specs/2026-10-14-webtoon-personal-site-design.md](file:///Users/gcg/Work/src/github.com/gcg/gcg.github.io/docs/superpowers/specs/2026-10-14-webtoon-personal-site-design.md)

## Global Constraints

- Zero external libraries or npm runtime dependencies: pure vanilla web stack.
- Work strictly on branch `redesign-webtoon`; never push to `main`.
- Clean, responsive mobile-first reading flow that scales to cinematic desktop monitors.
- Preserve existing personal portrait (`static/gcg.jpg` -> `assets/img/gcg.jpg`) and favicons.
- Exact timelines and copy:
  - 23 years tinkering with computers, servers, infrastructure, tools, automations.
  - Distro journey: Ubuntu (3-4 yrs) -> Gentoo (5 yrs) -> Arch (5 yrs) -> Fedora (Current / ever since, "sorry, no Arch btw").
  - Language journey: Ruby on Rails -> PHP (~2008) -> Laravel (~2014) -> Go (~2017) -> Gleam (~2 years ago).
  - Infra scope: Full spectrum, from plugging cables into physical routers/servers to managing large-scale infra on AWS & Google Cloud.
  - Poltio: 12 years co-founder and CTO ("make sure coworkers and clients never notice my existence by ensuring everything always works and nothing breaks") -> LinkedIn redirect.
  - Personal projects: Android apps mdwriter (`https://github.com/gcg/mdwriter`), wpchanger (`https://github.com/gcg/wpchanger`), and upcoming social messaging & gaming app teaser -> GitHub redirect (`https://github.com/gcg`).
  - `@gcg` identity: Constant handle with rotating Twitter/X, Instagram, and GitHub icon beacon.

## Review Focus

1. Mobile responsiveness: On viewports < 480px, ensure holographic status windows and timelines stack without horizontal scrolling or overlapping text.
2. Link integrity & security: All external links (GitHub, LinkedIn, Twitter/X, Instagram) must open in a new tab with `target="_blank"` and `rel="noopener noreferrer"`.
3. Performance & Reduced Motion: Ensure `prefers-reduced-motion` media queries disable intense continuous flashing/rotation animations for accessibility.
4. Social Icon Rotation Edge Cases: Hovering on the `@gcg` beacon must pause rotation so user can click accurately without the target switching under their cursor.
5. Local Dev Runner: `make` and `make serve` must cleanly start a local server at `http://localhost:8000` without requiring external package installations.

---

### Task 1: Clean Slate Setup, Asset Migration & Makefile

**Files:**
- Create: `Makefile`
- Create: `assets/img/`
- Create: `assets/favicons/`
- Modify: `.gitignore`
- Test: `tests/task1_verify.sh`

**Interfaces:**
- Consumes: `static/gcg.jpg`, `static/favicon*`, `static/apple-icon*`
- Produces: `assets/img/gcg.jpg`, `assets/favicons/`, root `Makefile` with targets `serve`, `clean`

- [ ] **Step 1: Write verification script for repository structure and Makefile**

```bash
# tests/task1_verify.sh
#!/bin/bash
set -e
test -f assets/img/gcg.jpg || { echo "Missing gcg.jpg"; exit 1; }
test -f assets/favicons/favicon.ico || { echo "Missing favicon.ico"; exit 1; }
grep -q "python3 -m http.server" Makefile || { echo "Makefile missing python http server"; exit 1; }
echo "Task 1 verification passed"
```

- [ ] **Step 2: Run verification script to confirm it fails**

Run: `bash tests/task1_verify.sh`
Expected: FAIL with "Missing gcg.jpg" or similar.

- [ ] **Step 3: Migrate assets, archive legacy Hugo files, and create modern Makefile**

1. Create `assets/img/` and copy `static/gcg.jpg` to `assets/img/gcg.jpg`.
2. Create `assets/favicons/` and copy favicons from `static/` to `assets/favicons/`.
3. Create `legacy-hugo-archive/` or remove obsolete Hugo directories (`themes/`, `archetypes/`, `layouts/`, `data/`, `resources/`, `content/`, `config.toml`, `.hugo_build.lock`) while keeping `public/` or clearing it.
4. Create modern `Makefile`:
   - `all: serve`
   - `serve: python3 -m http.server 8000`
   - `clean: rm -rf .DS_Store`
5. Update `.gitignore` for standard web files.

- [ ] **Step 4: Run verification script to confirm it passes**

Run: `bash tests/task1_verify.sh`
Expected: PASS with "Task 1 verification passed".

- [ ] **Step 5: Commit changes**

```bash
git add assets/ Makefile .gitignore tests/task1_verify.sh
git commit -m "chore: scaffold clean webtoon structure, migrate assets, and create makefile"
```

---

### Task 2: Solo Leveling Design Tokens & CSS Foundation

**Files:**
- Create: `assets/css/reset.css`
- Create: `assets/css/variables.css`
- Create: `assets/css/manhwa.css`
- Test: `tests/task2_css_verify.sh`

**Interfaces:**
- Consumes: Design spec Section 3 (Color palette, typography, glassmorphism, corner brackets)
- Produces: CSS custom properties (`--color-void`, `--color-cyan`, `--color-monarch`, `--glass-bg`, etc.), manhwa panel utility classes (`.system-window`, `.corner-brackets`, `.scanline-overlay`, `.comic-sfx`, `.gutter`)

- [ ] **Step 1: Write test script checking CSS token definitions and syntax**

```bash
# tests/task2_css_verify.sh
#!/bin/bash
set -e
grep -q -- "--color-cyan" assets/css/variables.css || { echo "Missing --color-cyan"; exit 1; }
grep -q -- "--color-monarch" assets/css/variables.css || { echo "Missing --color-monarch"; exit 1; }
grep -q "system-window" assets/css/manhwa.css || { echo "Missing .system-window"; exit 1; }
grep -q "prefers-reduced-motion" assets/css/manhwa.css || { echo "Missing reduced motion query"; exit 1; }
echo "Task 2 CSS tokens verified"
```

- [ ] **Step 2: Run verification script to confirm it fails**

Run: `bash tests/task2_css_verify.sh`
Expected: FAIL (files do not exist yet).

- [ ] **Step 3: Implement `reset.css`, `variables.css`, and `manhwa.css`**

1. `reset.css`: Modern box-sizing reset, default dark theme styling, smooth scrolling with `scroll-behavior: smooth`.
2. `variables.css`:
   - Void tones: `--bg-primary: #06070a`, `--bg-secondary: #0a0d14`, `--bg-card: rgba(16, 20, 31, 0.75)`
   - Neons: `--color-cyan: #00e5ff`, `--color-cyan-glow: rgba(0, 229, 255, 0.35)`, `--color-monarch: #a855f7`
   - Glassmorphism & Borders: `--border-hologram`, `--corner-bracket-size`
3. `manhwa.css`:
   - `.system-window`: Glassmorphic status panel with glowing border, corner HUD brackets (`::before`, `::after`), and header banner.
   - `.comic-sfx`: High-impact italic manhwa sound typography with neon drop shadow.
   - `.scanline-overlay`: Sweeping vertical hologram line animation.
   - `@media (prefers-reduced-motion: reduce)`: Disables infinite scanner and motion transforms.

- [ ] **Step 4: Run verification script to confirm it passes**

Run: `bash tests/task2_css_verify.sh`
Expected: PASS with "Task 2 CSS tokens verified".

- [ ] **Step 5: Commit changes**

```bash
git add assets/css/ tests/task2_css_verify.sh
git commit -m "style: implement solo leveling theme tokens, reset, and manhwa panel styles"
```

---

### Task 3: The Rotating `@gcg` Social Beacon Component

**Files:**
- Create: `assets/js/rotating-id.js`
- Test: `tests/task3_rotating_id_test.js`

**Interfaces:**
- Consumes: Target DOM element `#rotating-social-beacon`
- Produces: `initRotatingBeacon({ containerId, intervalMs, profiles })` class/function cycling Twitter/X, Instagram, and GitHub profiles with pause on hover.

- [ ] **Step 1: Write test script for rotating beacon state machine**

```javascript
// tests/task3_rotating_id_test.js
const assert = require('assert');
const { getNextProfile, PROFILES } = require('../assets/js/rotating-id.js');

assert.strictEqual(PROFILES.length, 3, "Expected 3 profiles");
assert.deepStrictEqual(PROFILES.map(p => p.id), ['github', 'twitter', 'instagram']);
assert.strictEqual(getNextProfile(0).id, 'twitter');
assert.strictEqual(getNextProfile(1).id, 'instagram');
assert.strictEqual(getNextProfile(2).id, 'github');
console.log("Task 3 rotating ID logic test passed");
```

- [ ] **Step 2: Run test script to verify it fails**

Run: `node tests/task3_rotating_id_test.js`
Expected: FAIL (module not yet created).

- [ ] **Step 3: Implement `assets/js/rotating-id.js`**

Implement:
- Array of `PROFILES`:
  - `github`: `https://github.com/gcg`, label `@gcg on GitHub`, inline SVG
  - `twitter`: `https://twitter.com/gcg`, label `@gcg on X / Twitter`, inline SVG
  - `instagram`: `https://instagram.com/gcg`, label `@gcg on Instagram`, inline SVG
- Pure function `getNextProfile(currentIndex) -> Profile`
- `class RotatingBeacon`:
  - Renders the constant `@gcg` text and active rotating icon pill.
  - Automatically advances active profile every 3500ms using CSS 3D flip animation.
  - `mouseenter`: Pauses timer and keeps current icon stable.
  - `mouseleave`: Resumes rotation timer.
  - Ensures clean click behavior directly opening the active profile in a new tab.
- Exports for both browser (`window.RotatingBeacon`) and Node/CommonJS (for automated tests).

- [ ] **Step 4: Run test to verify it passes**

Run: `node tests/task3_rotating_id_test.js`
Expected: PASS with "Task 3 rotating ID logic test passed".

- [ ] **Step 5: Commit changes**

```bash
git add assets/js/rotating-id.js tests/task3_rotating_id_test.js
git commit -m "feat: implement rotating @gcg social beacon component"
```

---

### Task 4: Interactive Hunter FX & Scroll Observer

**Files:**
- Create: `assets/js/hunter-fx.js`
- Test: `tests/task4_hunter_fx_test.js`

**Interfaces:**
- Consumes: Spec Section 5.2 (IntersectionObserver scroll reveals, stat counter animators, interactive scanline trigger)
- Produces: `initHunterFx()` wiring `.system-window` reveals, `.counter-val` tick-ups, and portrait hologram interactions.

- [ ] **Step 1: Write test for counter animation interpolation logic**

```javascript
// tests/task4_hunter_fx_test.js
const assert = require('assert');
const { formatStatValue } = require('../assets/js/hunter-fx.js');

assert.strictEqual(formatStatValue(23, 'int'), '23');
assert.strictEqual(formatStatValue(99.999, 'percent'), '99.999%');
assert.strictEqual(formatStatValue(12, 'int'), '12');
console.log("Task 4 hunter-fx logic test passed");
```

- [ ] **Step 2: Run test script to verify it fails**

Run: `node tests/task4_hunter_fx_test.js`
Expected: FAIL (hunter-fx.js not yet created).

- [ ] **Step 3: Implement `assets/js/hunter-fx.js`**

Implement:
- `formatStatValue(value, format)` helper.
- `animateCounter(element, target, duration, format)` using `requestAnimationFrame` with ease-out curve.
- `initScrollObserver()`: Sets up `IntersectionObserver` on `.reveal-on-scroll`. When target is visible:
  - Adds `.revealed` class.
  - Triggers child counters if any (`data-target-val`, `data-format`).
  - Illuminates sequential timeline steps.
- `initPortraitFX()`: Adds click/hover listener to re-trigger the holographic scanline animation and mana pulse on the hunter portrait.
- `initCodeGridParallax()`: Subtle parallax effect moving background syntax tokens based on scroll position and subtle mouse movement on desktop.
- UMD/browser export for script tag inclusion.

- [ ] **Step 4: Run test to verify it passes**

Run: `node tests/task4_hunter_fx_test.js`
Expected: PASS with "Task 4 hunter-fx logic test passed".

- [ ] **Step 5: Commit changes**

```bash
git add assets/js/hunter-fx.js tests/task4_hunter_fx_test.js
git commit -m "feat: implement hunter FX, dynamic counters, and scroll reveals"
```

---

### Task 5: Webtoon Narrative Assembly (`index.html` & `assets/css/style.css`)

**Files:**
- Create: `index.html`
- Create: `assets/css/style.css`
- Create: `assets/js/main.js`
- Test: `tests/task5_dom_verify.sh`

**Interfaces:**
- Consumes: `assets/css/reset.css`, `assets/css/variables.css`, `assets/css/manhwa.css`, `assets/js/rotating-id.js`, `assets/js/hunter-fx.js`, `assets/img/gcg.jpg`
- Produces: Complete, accessible single-page webtoon document fulfilling all spec requirements.

- [ ] **Step 1: Write DOM structure verification script**

```bash
# tests/task5_dom_verify.sh
#!/bin/bash
set -e
grep -q "Guney Can Gokoglu" index.html || { echo "Missing owner name"; exit 1; }
grep -q "rotating-social-beacon" index.html || { echo "Missing beacon container"; exit 1; }
grep -q "Ubuntu" index.html || { echo "Missing Ubuntu in distro timeline"; exit 1; }
grep -q "Gentoo" index.html || { echo "Missing Gentoo in distro timeline"; exit 1; }
grep -q "Arch" index.html || { echo "Missing Arch in distro timeline"; exit 1; }
grep -q "Fedora" index.html || { echo "Missing Fedora in distro timeline"; exit 1; }
grep -q "Ruby on Rails" index.html || { echo "Missing Rails in language timeline"; exit 1; }
grep -q "Gleam" index.html || { echo "Missing Gleam in language timeline"; exit 1; }
grep -q "Poltio" index.html || { echo "Missing Poltio raid section"; exit 1; }
grep -q "mdwriter" index.html || { echo "Missing mdwriter artifact"; exit 1; }
grep -q "wpchanger" index.html || { echo "Missing wpchanger artifact"; exit 1; }
grep -q "AWS" index.html || { echo "Missing AWS in infra scope"; exit 1; }
grep -q "Google Cloud" index.html || { echo "Missing Google Cloud in infra scope"; exit 1; }
echo "Task 5 DOM markup verified"
```

- [ ] **Step 2: Run verification script to confirm it fails**

Run: `bash tests/task5_dom_verify.sh`
Expected: FAIL (index.html does not yet contain these elements).

- [ ] **Step 3: Implement `index.html`, `style.css`, and `main.js`**

1. `index.html`:
   - **Header HUD**: Fixed status bar with system pulse indicator, player status `[ACTIVE]`, and the `#rotating-social-beacon` (`@gcg` + rotating icon).
   - **Background Layer**: Atmospheric code syntax grid containing real PHP/Laravel, Go, and Gleam snippets floating at subtle opacity.
   - **Prologue (Hero)**:
     - Notification banner: `[SYSTEM NOTIFICATION: PLAYER 001 CONNECTED — 23 YEARS ONLINE]`.
     - Hunter ID Card: Portrait `assets/img/gcg.jpg` inside the holographic scanner frame, `LV. 23`, `Stealth Architect / System Guardian`.
     - Punchy lore summary of 23 years of tinkering, infrastructure, servers, and tools.
   - **Chapter 1: The Core Engine & The Two Timelines**:
     - Full-Spectrum Infra Trait: Highlight spanning from plugging cables to routers/servers in racks up to orchestrating large infrastructure on AWS and Google Cloud.
     - Distro Evolution: Ubuntu (3-4 yrs) -> Gentoo (5 yrs) -> Arch (5 yrs) -> Fedora (Current / ever since, *"sorry, no Arch btw"*).
     - Language Evolution: Ruby on Rails -> PHP (2008) -> Laravel (2014) -> Go (2017) -> Gleam (2 yrs ago).
     - Passive Skill Window: `[Zero-Downtime Observer]` (*"Maintains absolute uptime so coworkers and clients never notice your existence"*).
     - Primary Stats: `Uptime: 99.999%`, `Resilience: S-Rank`, `Invisibility: MAX`.
   - **Chapter 2: The 12-Year Raid (Poltio)**:
     - Co-founder and CTO for 12 years. Scaleup architecture story.
     - Dungeon Gate CTA: `[VIEW FULL RAID DOSSIER ON LINKEDIN]` linking to LinkedIn.
   - **Chapter 3: Equipped Artifacts & The Lab**:
     - Artifact 1: [mdwriter](https://github.com/gcg/mdwriter) — Android markdown editor.
     - Artifact 2: [wpchanger](https://github.com/gcg/wpchanger) — Android wallpaper changer.
     - Artifact 3: [CLASSIFIED / IN FORGE] — Upcoming social messaging & gaming app teaser with glowing security lock.
     - CTA Portal: `[EXPLORE MORE ON GITHUB]` linking to `https://github.com/gcg`.
   - **Epilogue**: Webtoon `[CHAPTER COMPLETE: TO BE CONTINUED]` end card, contact links, copyright, and Fedora badge.
2. `style.css`:
   - Layout rules, responsive CSS Grid / Flexbox breakpoints, typography styles, button styles, hover glow enhancements.
3. `main.js`:
   - Bootstraps `RotatingBeacon` and `HunterFx`.

- [ ] **Step 4: Run verification script to confirm it passes**

Run: `bash tests/task5_dom_verify.sh`
Expected: PASS with "Task 5 DOM markup verified".

- [ ] **Step 5: Commit changes**

```bash
git add index.html assets/css/style.css assets/js/main.js tests/task5_dom_verify.sh
git commit -m "feat: complete webtoon narrative markup, styles, and chapter components"
```

---

### Task 6: End-to-End Verification, Responsive Testing & Dev Server

**Files:**
- Create: `tests/e2e_server_test.sh`
- Modify: `README.md`
- Test: `tests/e2e_server_test.sh`

**Interfaces:**
- Consumes: `Makefile`, `index.html`, all assets
- Produces: Verified working local site, passing E2E tests, updated README.

- [ ] **Step 1: Write end-to-end local server test script**

```bash
# tests/e2e_server_test.sh
#!/bin/bash
set -e
# Start local server in background
python3 -m http.server 8000 &
PID=$!
sleep 2

# Verify HTTP 200 and expected payload
curl -s -I http://localhost:8000 | grep -q "200 OK" || { echo "Failed HTTP 200"; kill $PID; exit 1; }
curl -s http://localhost:8000 | grep -q "Solo Leveling" || { echo "Missing page content"; kill $PID; exit 1; }

# Kill background server
kill $PID
echo "E2E server test passed!"
```

- [ ] **Step 2: Run E2E test script to verify it passes**

Run: `bash tests/e2e_server_test.sh`
Expected: PASS with "E2E server test passed!".

- [ ] **Step 3: Update README.md with project overview and local preview instructions**

Update `README.md` documenting:
- Project theme (Solo Leveling / Webtoon single-page personal site for Guney Can Gokoglu).
- How to preview locally: run `make` or `make serve` and visit `http://localhost:8000`.
- Pure vanilla architecture notes.

- [ ] **Step 4: Commit changes and final polish**

```bash
git add README.md tests/e2e_server_test.sh
git commit -m "docs: update README with dev instructions and add E2E verification test"
```
