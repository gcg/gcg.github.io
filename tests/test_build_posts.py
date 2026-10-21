import importlib.util
import os
import re
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("build_posts", os.path.join(ROOT, "scripts", "build_posts.py"))
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)

START, END = "<!-- CHRONICLES_START -->", "<!-- CHRONICLES_END -->"
POSTS = [
    {"slug": "b", "title": "Vim & <Lua>", "date": "2024-01-01"},
    {"slug": "a", "title": "Hello", "date": ""},
]


def read_index():
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        return f.read()


class PostYear(unittest.TestCase):
    def test_post_year(self):
        self.assertEqual(bp.post_year("2024-02-01T14:33:01+03:00"), "2024")
        self.assertEqual(bp.post_year(""), "")
        self.assertEqual(bp.post_year(None), "")
        self.assertEqual(bp.post_year("soon"), "")


class RenderPavilion(unittest.TestCase):
    def test_render_pavilion_escapes_and_orders(self):
        out = bp.render_pavilion(POSTS)
        b = '<a href="posts/b/">Vim &amp; &lt;Lua&gt;</a><span class="scroll-year">2024</span>'
        a = '<a href="posts/a/">Hello</a><span class="scroll-year"></span>'
        self.assertIn(b, out)
        self.assertIn(a, out)
        self.assertLess(out.index("posts/b/"), out.index("posts/a/"))


class SyncHomepage(unittest.TestCase):
    def _tmp(self, content):
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        self.addCleanup(os.remove, path)
        return path

    def test_sync_homepage_is_idempotent(self):
        path = self._tmp(f'<ol class="scrolls">{START}old{END}</ol>')
        self.assertTrue(bp.sync_homepage(POSTS, path))
        self.assertTrue(bp.sync_homepage(POSTS, path))
        with open(path, encoding="utf-8") as f:
            out = f.read()
        self.assertEqual(out.count("scroll-row"), 2)
        self.assertNotIn("old", out)

    def test_sync_homepage_without_markers(self):
        original = "<ol class=\"scrolls\"></ol>"
        path = self._tmp(original)
        self.assertFalse(bp.sync_homepage(POSTS, path))
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read(), original)


def content_posts():
    """(slug, date, draft) for every post source in content/posts."""
    out = []
    for entry in sorted(os.listdir(bp.CONTENT_DIR)):
        path = os.path.join(bp.CONTENT_DIR, entry)
        md = os.path.join(path, "index.md") if os.path.isdir(path) else path
        if not md.endswith(".md") or not os.path.isfile(md):
            continue
        with open(md, encoding="utf-8") as f:
            meta, _ = bp.parse_frontmatter(f.read())
        slug = entry if os.path.isdir(path) else entry[:-3]
        out.append((slug, str(meta.get("date", "")), str(meta.get("draft", "")).lower() in ("true", "yes", "1")))
    return out


class RealBuild(unittest.TestCase):
    @unittest.skipUnless('class="scrolls"' in read_index(), "homepage pavilion markup not built yet")
    def test_build_lists_every_published_post_newest_first(self):
        r = subprocess.run(["python3", "scripts/build_posts.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = read_index()
        block = html[html.index(START):html.index(END)]
        listed = re.findall(r'href="posts/([^/"]+)/"', block)
        published = {slug: date for slug, date, draft in content_posts() if not draft}
        self.assertCountEqual(listed, published.keys())
        dates = [published[s] for s in listed]
        self.assertEqual(dates, sorted(dates, reverse=True), "pavilion is not newest first")
        for s in listed:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "posts", s, "index.html")), s)


class Drafts(unittest.TestCase):
    def test_build_skips_and_prunes_drafts(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp))
        content, output = os.path.join(tmp, "content"), os.path.join(tmp, "posts")
        posts = {
            "live": "---\ntitle: Live\ndate: 2024-01-01\n---\n\nA published scroll with enough words.\n",
            "secret": "---\ntitle: Secret\ndate: 2025-01-01\ndraft: true\n---\n\nNot ready yet, keep it sealed.\n",
        }
        for slug, text in posts.items():
            os.makedirs(os.path.join(content, slug))
            with open(os.path.join(content, slug, "index.md"), "w", encoding="utf-8") as f:
                f.write(text)
        os.makedirs(os.path.join(output, "secret"))  # stale output from before it became a draft
        for name, value in (("CONTENT_DIR", content), ("OUTPUT_DIR", output)):
            old = getattr(bp, name)
            setattr(bp, name, value)
            self.addCleanup(setattr, bp, name, old)
        built = bp.build_posts()
        self.assertEqual([p["slug"] for p in built], ["live"])
        self.assertTrue(os.path.isfile(os.path.join(output, "live", "index.html")))
        self.assertFalse(os.path.exists(os.path.join(output, "secret")))


if __name__ == "__main__":
    unittest.main()
