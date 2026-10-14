# Guney Can Gokoglu (@gcg) &bull; Personal Site

A single-page personal portfolio and digital presence inspired by a **Solo Leveling / Action Manhwa "System Window"** webtoon aesthetic.

## Narrative & Highlights

- **23 Years of Mastery**: Tinkering with computers, maintaining servers, architecting resilient infrastructures, building tools and automations.
- **Full-Spectrum Infrastructure**: Spanning from physical bare-metal (crimping cables, racking switches/routers) to multi-region cloud hyperscale on AWS & Google Cloud.
- **The Distro Journey**: Ubuntu (3-4 yrs) &rarr; Gentoo (5 yrs compiling kernels) &rarr; Arch (5 yrs rolling release) &rarr; **Fedora** (Ever since; daily driver).
- **Language Grimoire**: Ruby on Rails &rarr; PHP (~2008) &rarr; Laravel (~2014) &rarr; Go (~2017) &rarr; Gleam (~2 yrs ago).
- **The 12-Year Raid (Poltio)**: Co-founder & CTO for 12 years—keeping platforms bulletproof so nobody notices.
- **Artifacts & The Lab**: Android apps ([mdwriter](https://github.com/gcg/mdwriter), [wpchanger](https://github.com/gcg/wpchanger)) and upcoming social messaging & gaming app teaser.
- **The Identity Anchor**: Constant `@gcg` handle with an orbiting rotating social beacon cycling GitHub, X / Twitter, and Instagram.

---

## Architecture

- **Pure Vanilla Web**: Semantic HTML5, modern CSS3 (Custom properties, grid, flexbox, glassmorphism, animations), and vanilla ES6+ JavaScript.
- **Zero Dependencies**: No node_modules, no bundlers, no external frameworks.
- **Static Hosting**: Ready for GitHub Pages (`https://gcg.me` / `https://gcg.github.io`).

---

## Local Development

To run the site locally:

```bash
make
# or
make serve
```

This starts Python's built-in HTTP server at:
**[http://localhost:8000](http://localhost:8000)**

---

## Tests & Verification

Automated test verification scripts are located in `tests/`:

```bash
bash tests/task1_verify.sh
bash tests/task2_css_verify.sh
node tests/task3_rotating_id_test.js
node tests/task4_hunter_fx_test.js
bash tests/task5_dom_verify.sh
bash tests/e2e_server_test.sh
```
