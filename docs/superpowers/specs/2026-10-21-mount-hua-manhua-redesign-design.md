# gcg.me redesign: "The Nameless Formation Master"

- **Date:** 2026-10-21
- **Branch:** `redesign-manhwa`
- **Owner:** Guney Can Gokoglu (@gcg)
- **Status:** approved 2026-10-21
- **Replaces:** the Solo Leveling "system window" design from 2026-10-14 (`2026-10-14-webtoon-personal-site-design.md`)

## 1. Intent

gcg.me is Guney's personal corner of the internet. It is **not** a portfolio, a sales page, or a consulting pitch.

Guney's two big loves are cultivation manhua/manhwa/webtoons and tech: Linux, open source, programming, infra, tinkering. The site should feel like opening a **full-colour Korean murim webtoon** whose protagonist is Guney.

The previous Gemini-built version was themed, but it was "just some rectangles put together". This redesign has to **read like an actual webtoon chapter**:
- painted scenes,
- glowing sword-qi effects,
- dramatic lettering,
- narration boxes, speech bubbles and SFX,
- a vertical scroll like the Webtoon app.

### Art references
Guney's three favourite art styles, all full-colour Korean murim webtoons:
- *Return of the Blossoming Blade*. Its Mount Hua plum-blossom sword sect is where the Mount Hua theme comes from.
- *Reincarnation of the Fist King*.
- *The Heavenly Demon Wants a Quiet Life*.

The target is their look: luminous, crisp digital painting, dramatic light, rich colour, and glowing technique effects.

### Who it's for
A fellow nerd who's into Linux, programming and infra, and quite possibly reads webtoons too. After two minutes on the page they should know:

1. **Guney has been around.** Linux since 2001, about 25 years of building things.
2. **The tinkering is for love.** Programming, infra and GNU/Linux are a hobby and a passion first, and only sometimes the job.
3. **Guney has left a mark** on open source and tech, in their own way. For now this is carried by the registry, the creed and the treasures. Content gets optimized after the design is final.

### Goals
- A vertical webtoon chapter in Mount Hua style, set in an Estonian winter, with a day version and a moonlit night version.
- Show off the four matching **@gcg** handles (GitHub, X, Instagram, Mastodon) near the top.
- Poltio (co-founder & CTO, 12 years) is the main arc.
- Show the side projects: 2 Android apps, plus 2 web apps "coming soon".
- Keep the blog, with posts restyled in the same world.
- Link the CV.
- Express "a good system architect is never noticed" in cultivation terms. Guney is **无名阵师, the Nameless Formation Master**.

### Non-goals
- No photos of Guney anywhere on the site. The protagonist appears only as a painted figure seen from behind, face unseen.
- No "hire me", no services list, no client logos, no conversion stats or business metrics.
- No career timeline beyond Poltio and the distro/language progression.
- No separate open-source section (for now).
- No CMS, framework, bundler, or node toolchain.

### Anti-goals (a failure even if it technically works)
- It looks like cards and rectangles with a theme sprinkled on, instead of a webtoon.
- Neon "system window" UI panels in the Solo Leveling sense. Guney explicitly rejected one.
  - Glowing *qi effects in the art* are wanted. Glowing *UI boxes* are not.
- Anything that reads as a **Japanese flag**, such as a red disc on a pale sky. Suns and moons are white or pale.
- Decoration that hides the tech. The commands, code and real facts must stay real.

## 2. Constraints

- **Hosting:** GitHub Pages at `gcg.me` (keep `CNAME`), deployed by the existing `.github/workflows/pages.yaml`, which runs `make build` and then uploads the repo root.
- **Stack:** vanilla HTML, CSS and JS, plus the existing zero-dependency Python post generator (`scripts/build_posts.py`, run by `make build`). No new runtime or build dependencies.
- **Fonts are self-hosted** (Guney's decision; no requests to Google).
  - The Chinese brush font is several MB in full, so it gets cut down to only the characters the site uses.
  - Cutting it down is a one-off offline step (e.g. `pyftsubset` from fonttools); it is not part of `make build`.
  - Note in the repo how to re-run it when new Chinese text is added.
- **Painted art comes from Guney's Figma connector,** on the **"guney's team"** plan (Starter: 500 AI credits a month, 150 a day).
  - Image generation is text-to-image only. No photos are ever uploaded.
  - Before each batch of generations, say how many images it is.
  - The image links Figma returns expire after 7 days, so download each image immediately.
  - Prompts must describe the style generically and never name a specific series.
- **Accessibility:**
  - Honour `prefers-reduced-motion` (stop petals, snow and qi animations).
  - Decorative art gets `aria-hidden` or empty `alt`.
  - All Chinese text is marked `lang="zh"`.
  - Chinese that carries meaning has an English equivalent: visible where the design shows it (title, arc, creed, registry, technique name), screen-reader-only where it doesn't (realm names; e.g. 练气 = Qi Refining).
  - Purely decorative Chinese (SFX like 唰!!, 封印 talismans, side rails) is `aria-hidden`.
  - The approved composition wins over adding visible captions. *(my call)*
  - Text contrast meets WCAG AA in both themes. Text over painted art gets a shadow, scrim or box as needed.
- **Mobile:** works at phone width with no horizontal scroll. Painted panels scale with the column and keep their aspect ratio.
- **Weight:** the painted art ships as optimized WebP or JPEG sized for the column (about 1.5–2× a 600px column). Images below the cover lazy-load.

## 3. The look

### 3.1 World
The setting is **Mount Hua in an Estonian winter**.

The Estonian flag is sky blue, black and white, inspired by winter: blue sky, the black treeline of the forests, and white snow on the ground. The flag shows up only as landscape, never as a literal flag.

Mount Hua brings:
- towering granite needle spires with snow on the ledges,
- a sea of clouds, pines clinging to cliffs, and a temple pavilion on a far summit,
- **plum blossoms** (梅花), Mount Hua's signature flower, which famously bloom in snow.

Pink plum blossom is the one warm accent.

### 3.2 Two layers
1. **Painted layer (raster, AI-generated).** The scenes: cover, hero, cliff, and the page backdrop. Each has a day and a night painting.
2. **Code layer (HTML, CSS, SVG) on top.** All lettering, talismans, narration boxes, speech bubbles, SFX, sword-qi arcs and bursting blossoms, falling petals, text panels, links and the theme toggle.
   - Text never gets baked into a painting.

### 3.3 Approved reference: cover, day
`.superpowers/redesign-assets/ai/cover-bg-day.png` (928×1152) is **approved**. It shows:
- a deep blue sky with a white sun upper right,
- a snow-dusted plum branch with pink blossoms and red buds entering from the top left,
- a sea of clouds with a pavilion on a left cliff,
- central granite needles, a tall cliff at the right with pines,
- a black pine forest and a white snowfield in the foreground.

Its prompt is in Appendix A. Every other painting must look like it came from the same artist: same rendering, line quality, palette and light.

### 3.4 Night ("Mount Hua by moonlight")
- **Every painted scene gets a night painting:**
  - a deep Estonian-blue night sky with stars,
  - a pale full moon (never red),
  - snow glowing under moonlight, so blue, black and white still read,
  - plum blossoms catching the light.
- **Code layer at night:**
  - text panels become dark paper with silver ink,
  - speech bubbles stay white with dark text,
  - petals and qi glow more strongly.
- **Theme switching:**
  - Follows the visitor's `prefers-color-scheme` by default, with a small toggle that persists in `localStorage`.
  - The saved theme must be applied **before first paint**, with no flash. The current `theme-toggle.js` applies it only after parsing, so it needs an inline snippet in `<head>`.
  - Painted images swap per theme, e.g. via `<picture>`, CSS, or a class.

### 3.5 Palette (code layer)
| Role | Day | Night |
|---|---|---|
| Page background | painted backdrop, fading into `#d4e3f3` → `#f6f9fc` | painted backdrop, fading into `#050c18` → `#0f1d33` |
| Text panel paper | `#fbfcfd` | `#101826` |
| Ink (borders, text) | `#14161a` | `#e6edf5` (borders `#c7d3e3`) |
| Plum blossom | `#ff8fb8`, `#ffa6c9`, `#ff7aa8`, buds `#d81b60` | same |
| Sword qi glow | `#ff5c9a` → `#ffd1e3` → white core | same, stronger bloom |
| Accent / labels / technique names | cinnabar `#b4233c` | `#e0435f` |
| Narration box | `#0b1030d9` with white italic text and a `#ff6f9f` left rule | same |

### 3.6 Typography (all self-hosted)
| Use | Font |
|---|---|
| Chinese brush (titles, SFX, technique and realm names) | **Ma Shan Zheng**, subset |
| English display (name, small epic caps) | **Cinzel**, 600 and 800 |
| English body and narration | **Cormorant Garamond** |
| Speech bubbles and hand-lettered lines | **Shantell Sans**, bold |
| Commands and code | **JetBrains Mono** |

Big brush lettering (the cover title, technique names, SFX) gets:
- a white or gradient fill,
- a dark outline (`paint-order: stroke`),
- a pink glow.

That's the webtoon title-card look from the spike.

### 3.7 Panel language
- **Strip:** a single centred column, max about 600px.
- **Scene panels** (cover, hero, cliff): **full-bleed painted panels with no border**, like Korean webtoons. They are separated by generous vertical space (about 40px).
- **Text panels** (registry, arc title, creed, treasures, blog, ending): ink-and-paper panels with 3px ink borders and slightly uneven corners, sitting on the backdrop. They must feel like part of the same painted world, not UI cards.
  - The approved ink "sect registry" from the earlier mockups is the baseline.
  - Neon is not allowed.
- **Narration boxes:** a dark translucent box with white italic serif text and a pink left rule.
- **Speech bubbles:** white ovals with an ink border and a tail.
- **SFX:** huge brush characters, rotated, with outline and glow.
- **Technique call-outs** (murim trope): the brush name, a small Cinzel English subtitle, and a real command in a mono chip.
- **Side rails** (wide screens): faint vertical calligraphy in the margins, e.g. 华山 · 无名阵师.

### 3.8 Atmosphere
- **Backdrop:**
  - A wide painted Mount Hua range (day and night), fixed behind the strip, so the chapter scrolls over it.
  - Wide screens see more of it.
  - It fades or mists into the page background at the edges and bottom.
- **Falling petals:** Guney loved these and asked for more.
  - About 60 small plum petals and snowflakes behind the strip, plus a few large, blurred petals in front for depth.
  - They flutter in 3D and drift sideways.
  - Code only; disabled under reduced motion.
- **Sword qi:** in the hero panel, glowing pink arcs draw themselves in around the sword, with blossoms bursting outward. Code layer, SVG.
- **Talismans:** sway gently.

## 4. The page, top to bottom

Visual references (local only, in gitignored `.superpowers/`):
- `brainstorm/47249-1792568428/content/compare-ai-v2.html`: the approved cover (B).
- `spike-murim-v2.html`: the hero composition, the qi effect and the lettering style.
- `hua-v6.html` / `hua-v7-night.html`: the structure and the text-panel styling for the registry, creed, treasures, blog and ending.

Their sources are in `.superpowers/redesign-assets/mockup-src/`. They are references, not code to ship.

Copy marked **(draft)** is my wording in the voice Guney approved. Content gets a pass after the design is final.

### Panel 1 · Cover (scene panel)
- **Background:** the approved painted cover (day), plus a night painting of the same composition.
- **Talismans:**
  - Four paper talismans hang from the top-right edge.
  - Each is a link, with vertical text: `github @gcg`, `x @gcg`, `insta @gcg`, `mastodon @gcg`.
  - This is the "show off the handle" moment.
- **Title:** large vertical brush lettering **无名阵师** on the right, below the talismans.
- **Lower left, over the dark trees:**
  - small caps "The Nameless Formation Master"
  - **Guney Can Gokoglu** in Cinzel
  - tagline (Guney's pick, from the motto "prepare for everything so nobody notices what you are doing"): **"If you saw me fight, I didn't prepare enough."**
- **Not on the cover:** no "LINUX" tag, no red seal box.

### Panel 2 · Hero (scene panel)
- **Painting:**
  - The protagonist **from behind**, standing on a snowy granite peak at blue hour, sword lowered at the right side.
  - Robes, a topknot with a flowing ribbon, and a plum-blossom emblem on the back of the robe.
  - Mount Hua spires and a cloud sea below, lit pink from the right by the sword's glow.
  - Night version: moonlit.
- **Same figure as Panel 4:** the robe colours, hair and build must match between the two paintings. Regenerate until they do.
- **Code layer:**
  - Glowing plum-blossom sword-qi arcs around the sword, drawing themselves in, with blossoms bursting outward.
  - Narration *(draft)*: "Tallinn, in winter. Twenty-five years since the first install."
  - SFX: 唰!!
  - Technique call-out: **梅花剑法 · Plum Blossom Sword Art · Form 25** with `$ sudo dnf upgrade --refresh` *(draft)*.

### Panel 3 · Sect registry (text panel)
This is the character sheet. It is ink style; neon is not allowed.
- **Header:** label `SECT REGISTRY`, title `修士 · Cultivator`. No seal.
- **Rows:**
  - **Name:** Guney Can Gokoglu · @gcg
  - **Dao:** GNU/Linux, cultivated since 2001
  - **Sect:** Poltio · Co-founder & CTO
  - **Sword forms:** numbered chips 一 Ruby · 二 PHP · 三 Laravel · 四 Go · 五 Gleam, in learning order (Ruby on Rails, PHP ~2008, Laravel ~2014, Go ~2017, Gleam ~2024).
- **Realm climb:** a mountain with a dashed path up to the summit and four stations:
  - 练气 Ubuntu · 3–4 yrs
  - 筑基 Gentoo · 5 yrs
  - 金丹 Arch · 5 yrs, btw
  - 元婴 Fedora · current realm. Highlighted, with a blossom at the summit.

### Panel 4 · Main arc: the Poltio Sect
- **Arc title (text panel):**
  - label `MAIN ARC · 2014 — NOW`
  - brush 第二卷 · 立宗 ("Volume Two · Founding the Sect")
  - "The Poltio Sect: Twelve Years"
  - a link to poltio.com
- **Cliff (scene panel):**
  - Painting: the same protagonist, from behind, seated or standing on a black rock ledge with a snowy lip, looking out over a misty Mount Hua range with a pavilion. Petals drift.
  - Night version: moonlit.
  - Narration top: "Twelve years ago, a sect was founded."
  - Narration bottom: "Some build a sect to be remembered. Others build one that simply never falls."
- **Removed on purpose:** Guney cut the "first line of code", "millions of visitors / $1–2K a month" and "AWS → GCP migration" beats. Do not reintroduce Poltio stats or migration stories.

### Panel 5 · The Formation Master's Creed (text panel)
- **Left:** vertical brush text 善战者 / 无智名 / 无勇功.
- **Right:**
  - label `THE FORMATION MASTER'S CREED`
  - "Those who fight well earn no fame for wisdom, and no credit for courage." — Sun Tzu, *The Art of War*, IV
  - twist line *(draft)*: "The best formation is the one no disciple ever notices. Twelve years. Nobody noticed. That was the point."
- **Meaning:** in cultivation novels a formation master builds the arrays that protect a sect, and a perfect array goes unnoticed. That's the system architect.
- **Optional second line:** 胜兵先胜而后求战, "the victorious army wins first, then seeks battle" (Sun Tzu IV).

### Panel 6 · Treasure Pavilion (text panel)
A 2×2 grid:
- **mdwriter**: Android artifact. Distraction-free markdown notes. Links to https://github.com/gcg/mdwriter.
- **wpchanger**: Android artifact. Wallpapers that rotate themselves. Links to https://github.com/gcg/wpchanger.
- **Two sealed treasures:**
  - A 封印 ("sealed") talisman and `SEALED · OPENING SOON`.
  - No names, no links.
  - Swapped by hand at launch.

### Panel 7 · Scripture Pavilion (text panel, blog)
- **Header:** label `藏经阁 · SCRIPTURE PAVILION · BLOG`.
- **Content:** scroll rows, newest first. Each row is the linked title with the year.
- **Generation:** generated by `scripts/build_posts.py` between the existing `<!-- CHRONICLES_START -->` / `<!-- CHRONICLES_END -->` markers. Title and year only, no post bodies.

### Panel 8 · Ending (text panel)
- **Content:**
  - 未完待续
  - *To be continued…*
  - "Read the full sect records (CV) ↗", linking to the CV PDF
  - a small LinkedIn link (https://www.linkedin.com/in/guneycan)

## 5. Blog post pages
- **Source:** Markdown in `content/posts/<slug>/index.md`, built to `posts/<slug>/index.html` via `scripts/build_posts.py` and `templates/post.html`.
- **Current posts:** 4.
- **Look:** same world as the homepage: painted backdrop, petals, day/night, and self-hosted fonts.
- **Layout:**
  - the post as one wide ink-and-paper "scripture scroll" panel,
  - a header strip with the title and date,
  - a way back to the Scripture Pavilion.
- Code blocks must stay readable in both themes.
- Re-theme the generator's lore strings (e.g. the default excerpt "Hunter system record…"). There must be no Solo Leveling vocabulary left anywhere.

## 6. Assets

### Painted art (to generate)
About 7 more images, each downloaded immediately and kept as a full-size PNG master in `.superpowers/redesign-assets/ai/` (gitignored). Only optimized versions are committed.

| Scene | Day | Night |
|---|---|---|
| Cover | ✅ approved | to generate |
| Hero, protagonist on peak | to generate | to generate |
| Cliff, protagonist on ledge | to generate | to generate |
| Backdrop, wide landscape | to generate | to generate |

- Generate the **day** versions first and show Guney before generating the night ones.
- Retries count against the 150-credits-a-day cap.

### Other assets
- **CV:** copy into the repo from `.superpowers/redesign-assets/Guney-Can-Gokoglu-CV.pdf`. It's public-facing and already lists gcg.me, the email and GitHub.
- **Favicon:** keep the existing favicons.
- **Remove** `assets/img/gcg.jpg`. No photos are used.

### Social URLs
| Talisman | URL |
|---|---|
| GitHub | https://github.com/gcg |
| X | https://twitter.com/gcg (or the x.com equivalent) |
| Instagram | https://instagram.com/gcg |
| Mastodon | https://phpc.social/@gcg (add `rel="me"`) |

## 7. What goes away
Everything specific to the Solo Leveling version:
- Code-syntax flanking rails, the "hunter" HUD nav, the rotating 3D social beacon, and stat counters.
- `hunter-fx.js`, `rotating-id.js`, `manhwa.css`, and the hunter/system-window CSS.
- "Episode" and "chapter" hunter lore.
- Gemini's `tests/` scripts, which check the old markup.

Reuse `theme-toggle.js`, `build_posts.py` and the Makefile wherever they still fit.

## 8. Left to the builder
- File and CSS architecture, class names, and how the code-layer SVG is authored.
- How themes swap images and colours.
- Exact panel sizes, spacing, breakpoints, and how overlays reposition on phones, as long as it still reads as a vertical webtoon.
- Image formats, sizes and lazy-loading details.
- Prompt wording for the remaining paintings, within §3.3 and Appendix A, including retries until the protagonist matches across the hero and cliff.
- What checks to leave behind. At minimum, one runnable check that `make build` produces the post pages and fills the Scripture Pavilion list.
- Copy polish on the *(draft)* lines, keeping the voice.

## 9. Calls I made that Guney should check
1. **Hero technique:** "Plum Blossom Sword Art · Form 25: `sudo dnf upgrade --refresh`". It's a Fedora command dressed as a sword form.
2. **Protagonist's look:** robes with a plum-blossom emblem on the back, a topknot with a ribbon, and a sword, always seen from behind.
3. **Small LinkedIn link** next to the CV link in the ending panel. It's not a talisman.
4. **Poltio arc links to poltio.com.**
5. **Blog list on the homepage** shows title and year only.
6. **Arc numbering:** the Poltio arc is labelled "Volume Two" (第二卷).
7. **Cinzel** added as the English display font, as in the spike.
8. **Old tests:** Gemini's `tests/` are deleted rather than ported.

## Appendix A · Approved cover prompt
Model: `gemini-3.1-flash-image`, via Figma `generate_image`, 1200×1520 requested (928×1152 returned).

> Vertical webtoon cover background illustration in Korean martial-arts (murim) manhwa style: full-colour digital painting, luminous, crisp, highly detailed, cinematic. Scene: the peaks of Mount Hua, towering sheer granite needle spires with snow resting on their ledges and a few pines clinging to the cliffs, rising out of a sea of soft white clouds; a small temple pavilion with upturned eaves on one distant summit. Crisp winter morning: deep vivid blue sky fading to pale near the horizon, a white sun glowing softly in the upper right with gentle light rays (the sun is white, never red). Lower part of the image: a dense black pine-forest treeline, and below it clean bright white snow in the foreground with subtle blue shadows. A blossoming plum branch with pink five-petal flowers and dark red buds enters from the top-left corner, a few pink petals drifting through the air. Colour palette built on blue, black and white (like the Estonian flag as a winter landscape) with pink plum blossom accents. No people, no characters, no text, no letters, no logos, no watermark. Leave calm open sky on the right side for a vertical title.

Figma file holding the generations: https://www.figma.com/design/zBgyhqtAIbuOi465lWdBka
