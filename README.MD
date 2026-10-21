# gcg.me

The personal site of Guney Can Gokoglu (@gcg), told as a chapter of a full-colour murim webtoon:
**无名阵师, The Nameless Formation Master**. It's Mount Hua in an Estonian winter, with painted
scenes, plum-blossom sword qi, falling petals, and a moonlit night version. The blog lives in the
Scripture Pavilion.

Plain HTML, CSS and a little JS, plus a zero-dependency Python script that builds the blog.
Deployed to GitHub Pages by `.github/workflows/pages.yaml`.

## Develop

```bash
make        # build posts and serve at http://localhost:8000
make test   # build, then run the checks in tests/
```

Write posts as Markdown in `content/posts/<slug>/index.md`. `make build` turns them into
`posts/<slug>/index.html` and refills the Scripture Pavilion list on the homepage.

## Art

The scenes in `assets/img/art/` were painted with Figma AI from text prompts, with no photos involved.
The prompts are in the design spec (`docs/superpowers/specs/2026-10-21-mount-hua-manhua-redesign-design.md`,
Appendix A, plus the plan's Task 1). The full-size masters are kept locally in `.superpowers/redesign-assets/`.

## Fonts

The fonts are self-hosted and subset (SIL OFL). After adding Chinese text, re-run `scripts/subset_fonts.sh`
(it needs fonttools and brotli; see the script header).
