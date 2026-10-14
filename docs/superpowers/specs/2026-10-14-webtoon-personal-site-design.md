# Design Specification: Webtoon Personal Website ("Solo Leveling" Aesthetic)

- **Date**: 2026-10-14
- **Branch**: `redesign-webtoon`
- **Owner**: Guney Can Gokoglu (@gcg)
- **Status**: Approved / Updated Spec with Timelines & Infra Range

---

## 1. Executive Summary & Goals

Transform the personal site of Guney Can Gokoglu (`gcg.github.io` / `gcg.me`) from a legacy Hugo blog into a single-page, high-craft personal portfolio with a **Solo Leveling / Action Manhwa "System Window"** webtoon aesthetic.

The site is built strictly with **vanilla HTML5, CSS3, and modern JavaScript (ES6+)**, with zero external frameworks, libraries, or build dependencies. It showcases 23 years of software tinkering, physical-to-cloud server infrastructure reliability, co-founding Poltio, open-source projects, and personal Android apps through an episodic vertical webtoon reading experience.

---

## 2. Narrative & Content Structure

The webpage reads as a vertical manhwa chapter titled **"Awakening: The Stealth Architect"**.

### 2.1 The Identity Anchor: `@gcg`
- **Header HUD**: Constant handle label `@gcg` paired with a rotating holographic orbit badge that cycles through **GitHub**, **Twitter / X**, and **Instagram**.
- **Behavior**: Smooth 3D flip every 3.5 seconds. Pauses on hover, displaying an active link tooltip. Clicking immediately opens the active profile.

### 2.2 Prologue: The Hunter Awakening (Hero Section)
- **System Announcement Banner**: `[SYSTEM NOTIFICATION: PLAYER 001 CONNECTED — 23 YEARS ONLINE]`
- **Hunter ID Card**:
  - Portrait: Guney Can Gokoglu (`assets/img/gcg.jpg`), housed in a holographic scanner frame with animated vertical scanlines, corner reticles (`┌ ┐ └ ┘`), and interactive mana glow on hover/click.
  - Class: `Stealth Architect / System Guardian`
  - Level: `LV. 23` (representing 23 years of hands-on software & systems mastery).
  - Subtitle: Co-founder & CTO at Poltio, infrastructure ninja, tools & automation craftsman.

### 2.3 Chapter 1: The Core Engine, Passive Skills & The Two Timelines
This chapter establishes Guney's deep roots through stats, passive abilities, and evolutionary timelines.

#### A. Full-Spectrum Infrastructure Trait
- **Physical to Cloud Mastery**: Highlight that Guney's infrastructure skills span from physical bare metal (plugging cables into switches, routers, and racking servers) up to managing complex, high-scale deployments on **AWS** and **Google Cloud**.
- **System Trait Badge**: `[TRAIT: FULL-SPECTRUM INFRASTRUCTURE — L1 BARE-METAL TO L7 MULTI-CLOUD]`.

#### B. The Distro Evolution (Path of the Penguin)
A horizontal or stepping manhwa milestone progression:
1. **Ubuntu** (3–4 years): The early adventuring days.
2. **Gentoo** (5 years): The crucible of source compilation and custom kernel tuning.
3. **Arch Linux** (5 years): The rolling-release mastery phase (*"I used Arch btw"*).
4. **Fedora** (Current / Ever Since): The battle-tested, refined workstation and server choice (*"Sorry, no Arch anymore—Fedora is home"*).

#### C. The Language Grimoire Evolution
A parallel milestone timeline:
1. **Ruby on Rails** (The Origin): Building dynamic web apps in the early days.
2. **PHP** (~2008): Stepping into robust, pragmatic backend development.
3. **Laravel** (~2014): Immediate love for modern expressive architecture and elegant DX.
4. **Go** (~2017): The concurrent powerhouse for high-performance systems and backend services.
5. **Gleam** (~2 Years Ago): The latest passion—type-safe functional programming on the BEAM.

#### D. Passive Skill Window
- **Skill Name**: `[Passive: Zero-Downtime Observer]`
- **Description**: *"Maintains absolute system resilience so coworkers and clients never notice your existence."*
- **Stats**: `Uptime: 99.999%`, `Resilience: S-Rank`, `Stealth: MAX`.

### 2.4 Chapter 2: The 12-Year Raid (Poltio)
- **Narrative**: Co-founder and CTO for 12 years. The epic scaleup campaign: architecting infrastructure, guiding engineering, and maintaining rock-solid uptime through rapid growth.
- **Quest Reward / Dossier CTA**:
  - Button styled as a high-tier dungeon gate: `[VIEW FULL RAID DOSSIER ON LINKEDIN]`, linking directly to Guney's LinkedIn profile.

### 2.5 Chapter 3: Equipped Artifacts & The Lab (Projects)
Presented as an inventory grid of hunter equipment:
1. **Artifact I: mdwriter**
   - Type: Android Markdown Editor App
   - Link: `https://github.com/gcg/mdwriter`
   - Description: Distraction-free, fast markdown note-taking for mobile.
2. **Artifact II: wpchanger**
   - Type: Android Wallpaper Changer App
   - Link: `https://github.com/gcg/wpchanger`
   - Description: Automated wallpaper rotation utility for Android devices.
3. **Artifact III: [CLASSIFIED / IN FORGE]**
   - Type: S-Rank Upcoming Social Messaging & Gaming App
   - Status: In active development. Encased in a glowing security vault / awakening aura.
4. **Full Inventory Link**:
   - `[EXPLORE MORE ON GITHUB]` linking directly to `https://github.com/gcg`.

### 2.6 Epilogue: Chapter Complete (Footer)
- End-of-chapter manhwa card: `[CHAPTER COMPLETE: TO BE CONTINUED]`.
- Direct social links, copyright notice, and tagline: *"Built with Vanilla Web Technologies on Fedora"*.

---

## 3. Visual & Aesthetic Design System

### 3.1 Color Palette
- **Obsidian Void (Background)**: `#06070a`, `#0a0d14`, `#10141f`
- **System Hologram Cyan (Primary Neon)**: `#00e5ff`, `#38bdf8`
- **Monarch Purple (Secondary Neon / S-Rank)**: `#a855f7`, `#7c3aed`
- **Card Glass Surface**: `rgba(16, 20, 31, 0.75)` with `backdrop-filter: blur(12px)`
- **Border Glow**: `1px solid rgba(0, 229, 255, 0.35)` with box shadows `0 0 20px rgba(0, 229, 255, 0.15)`
- **Text**: Primary `#f1f5f9`, Secondary `#94a3b8`, Accent Cyan `#38bdf8`

### 3.2 Atmosphere & Background Syntax Stream
Floating subtly in the background behind the content panels is a low-opacity (~8-12%) grid featuring real syntax from Guney's favorite technologies:
- **PHP / Laravel**:
  ```php
  Route::middleware(['auth:guardian', 'zero_downtime'])->group(function () {
      Cluster::keepAlive();
  });
  ```
- **Go**:
  ```go
  go func(infra *Cluster) {
      select {
      case <-ctx.Done():
          infra.GracefulShutdown()
      }
  }(infra)
  ```
- **Gleam**:
  ```gleam
  pub fn maintain_uptime(server: Server) -> Result(Status, Nil) {
      server |> monitor |> ensure_resilient
  }
  ```

---

## 4. File Structure & Architecture

```text
gcg.github.io/
├── index.html                  # Single-page webtoon markup
├── assets/
│   ├── css/
│   │   ├── reset.css           # Clean modern reset
│   │   ├── variables.css       # Theme tokens, colors, glassmorphism vars
│   │   ├── manhwa.css          # Webtoon panels, speech accents, sound typography
│   │   └── style.css           # Layouts, components, responsive styles
│   ├── js/
│   │   ├── main.js             # Initialization & event wiring
│   │   ├── rotating-id.js      # Cycling @gcg social icon mechanism
│   │   └── hunter-fx.js        # IntersectionObserver scroll animations, stat counters, photo scanline
│   ├── img/
│   │   └── gcg.jpg             # Profile photo (migrated from static/gcg.jpg)
│   └── favicons/               # Favicon assets
├── docs/
│   └── superpowers/specs/      # Design specs and planning docs
├── Makefile                    # Local runner (make / make serve)
└── README.md                   # Project documentation
```

---

## 5. Script Specifications

### 5.1 `rotating-id.js`
- Maintains an array of social profiles:
  - `github`: `https://github.com/gcg`, SVG GitHub icon
  - `twitter`: `https://twitter.com/gcg` (or `x.com/gcg`), SVG X/Twitter icon
  - `instagram`: `https://instagram.com/gcg`, SVG Instagram icon
- State machine flips through profiles every 3.5 seconds with a 3D flip animation.
- Pauses on mouse enter / resume on mouse leave.
- Accessible ARIA labels and title tooltips.

### 5.2 `hunter-fx.js`
- **IntersectionObserver**: Observes `.system-window` and `.manhwa-panel` elements. When scrolled into view, adds `.revealed` class triggering smooth entrance transitions.
- **Dynamic Stat Counters**: Animates numbers from `0` to target (`23` years, `99.999%` uptime, `12` years) when the attributes panel enters the viewport.
- **Hunter Portrait Scanner**: Interactive trigger on click/hover to replay the vertical scanline HUD effect and mana particle pulse.
- **Timeline Progression FX**: Illuminates the Linux and Language milestones sequentially as the user scrolls through them.
- **Parallax Code Particles**: Mild mouse-move tracking on desktop for background code tokens.

---

## 6. Makefile & Local Development

The [Makefile](file:///Users/gcg/Work/src/github.com/gcg/gcg.github.io/Makefile) will provide:
- `make` (default): Starts the local preview server on `http://localhost:8000`.
- `make serve`: Explicit alias for `python3 -m http.server 8000`.
- `make clean`: Cleans any temporary files.

---

## 7. Verification & Quality Gates

1. **Local Preview**: Verify `make serve` starts without error and the site renders cleanly in all modern browsers.
2. **Design Fidelity**:
   - Holographic Solo Leveling aesthetic with crisp glowing borders and glassmorphism.
   - Hunter photo scanline and status HUD rendering correctly.
   - Linux and Language timelines clearly rendered with their specific milestones.
   - Physical cable to cloud infra capability prominently featured.
   - Background syntax streams visible but subtle (~10% opacity).
3. **Interactivity**:
   - Rotating `@gcg` beacon cycles smoothly between GitHub, Twitter, and Instagram, and links are clickable.
   - Stat counters animate on scroll.
   - All external links open in new tabs with `rel="noopener noreferrer"`.
4. **Responsiveness**:
   - Clean vertical scroll experience on mobile screens (375px - 430px).
   - High-impact widescreen presentation on desktop displays (1024px+).
5. **Git Safety**:
   - All changes contained on `redesign-webtoon` branch; no pushes to `main`.
