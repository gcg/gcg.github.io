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


class RealBuild(unittest.TestCase):
    @unittest.skipUnless('class="scrolls"' in read_index(), "homepage pavilion markup not built yet")
    def test_build_skips_drafts_and_sorts_newest_first(self):
        r = subprocess.run(["python3", "scripts/build_posts.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = read_index()
        block = html[html.index(START):html.index(END)]
        slugs = re.findall(r'href="posts/([^/"]+)/"', block)
        self.assertEqual(slugs, [
            "technologies-i-am-investing-in-2024",
            "technologies-i-am-investing-in-2023",
            "neovim-lua",
            "hello-hugo",
        ])
        for s in slugs:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "posts", s, "index.html")), s)


if __name__ == "__main__":
    unittest.main()
