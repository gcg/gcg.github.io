import glob
import os
import re
import unittest
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pages():
    return [os.path.join(ROOT, "index.html")] + sorted(glob.glob(os.path.join(ROOT, "posts", "*", "index.html")))


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append(value)


def local_targets(page):
    parser = LinkCollector()
    with open(page, encoding="utf-8") as f:
        parser.feed(f.read())
    for link in parser.links:
        if re.match(r"^(https?:|mailto:|#|data:)", link):
            continue
        path = link.split("#", 1)[0].split("?", 1)[0]
        target = os.path.normpath(os.path.join(os.path.dirname(page), path))
        if link.endswith("/") or os.path.isdir(target):
            target = os.path.join(target, "index.html")
        yield link, target


class Site(unittest.TestCase):
    def test_local_links_resolve(self):
        missing = []
        for page in pages():
            for link, target in local_targets(page):
                if not os.path.exists(target):
                    missing.append(f"{os.path.relpath(page, ROOT)} -> {link}")
        self.assertEqual(missing, [], "missing local targets:\n" + "\n".join(missing))

    def test_css_urls_resolve(self):
        missing = []
        for css in glob.glob(os.path.join(ROOT, "assets", "css", "*.css")):
            with open(css, encoding="utf-8") as f:
                for url in re.findall(r"url\(['\"]?(?!data:|#)([^'\")]+)['\"]?\)", f.read()):
                    if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(css), url))):
                        missing.append(f"{os.path.basename(css)} -> {url}")
        self.assertEqual(missing, [], "missing CSS url() targets:\n" + "\n".join(missing))

    def test_no_solo_leveling_vocabulary(self):
        files = [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "templates", "post.html"),
                 os.path.join(ROOT, "scripts", "build_posts.py")]
        files += glob.glob(os.path.join(ROOT, "assets", "css", "*.css"))
        files += glob.glob(os.path.join(ROOT, "assets", "js", "*.js"))
        files += pages()[1:]
        banned = ["Hunter", "hunter", "Solo Leveling", "system-window", "Monarch", "Chronicle Log", "fonts.googleapis"]
        hits = []
        for path in files:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            hits += [f"{os.path.relpath(path, ROOT)}: {word}" for word in banned if word in text]
        self.assertEqual(hits, [])

    def test_reduced_motion_rules_exist(self):
        with open(os.path.join(ROOT, "assets", "css", "style.css"), encoding="utf-8") as f:
            css = f.read()
        m = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", css, re.S)
        self.assertIsNotNone(m, "no prefers-reduced-motion: reduce block")
        for selector in (".petals", ".qa", ".talisman"):
            self.assertIn(selector, m.group(1))


if __name__ == "__main__":
    unittest.main()
