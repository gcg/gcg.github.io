import glob
import os
import re
import unittest
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pages():
    return [os.path.join(ROOT, "index.html")] + sorted(glob.glob(os.path.join(ROOT, "posts", "*", "index.html")))


def _luminance(hex_colour):
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def theme_tokens():
    """Returns {block name: {token: hex}} for the day block and both night blocks in variables.css."""
    with open(os.path.join(ROOT, "assets", "css", "variables.css"), encoding="utf-8") as f:
        css = f.read()
    blocks = {
        "day": re.search(r":root \{(.*?)\n\}", css, re.S).group(1),
        "night (data-theme)": re.search(r':root\[data-theme="dark"\] \{(.*?)\n\}', css, re.S).group(1),
        "night (OS)": re.search(r':root:not\(\[data-theme="light"\]\) \{(.*?)\n  \}', css, re.S).group(1),
    }
    day = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})\b", blocks["day"]))
    out = {}
    for name, body in blocks.items():
        tokens = dict(day)
        tokens.update(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})\b", body))
        out[name] = tokens
    return out


class LangChecker(HTMLParser):
    """Records Chinese text that is not inside an element with lang="zh"."""
    VOID = {"meta", "link", "img", "br", "input", "hr", "source", "circle", "path", "ellipse", "rect", "stop", "feGaussianBlur", "feMergeNode"}

    def __init__(self):
        super().__init__()
        self.stack, self.unmarked = [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        lang = dict(attrs).get("lang")
        self.stack.append(lang if lang else (self.stack[-1] if self.stack else "en"))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        current = self.stack[-1] if self.stack else "en"
        for run in re.findall(r"[\u3000-\u9fff]+", data):
            if current != "zh":
                self.unmarked.append(run)


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

    def test_text_colours_meet_wcag_aa_on_paper(self):
        failures = []
        for theme, t in theme_tokens().items():
            for token in ("ink", "muted", "accent"):
                ratio = contrast(t[token], t["paper"])
                if ratio < 4.5:
                    failures.append(f"{theme}: --{token} {t[token]} on --paper {t['paper']} = {ratio:.2f}:1")
        self.assertEqual(failures, [])

    def test_glossary_explains_every_chinese_phrase(self):
        with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
            home = f.read()
        m = re.search(r'<details class="panel glossary".*?</details>', home, re.S)
        self.assertIsNotNone(m, "no glossary on the homepage")
        terms = re.findall(r"<dt[^>]*>(.*?)</dt>", m.group(0), re.S)
        pages_text = home.replace(m.group(0), "")
        with open(os.path.join(ROOT, "templates", "post.html"), encoding="utf-8") as f:
            pages_text += f.read()
        runs = set(re.findall(r"[\u3000-\u9fff]+", pages_text))
        missing = sorted(r for r in runs if not any(r in t for t in terms))
        self.assertEqual(missing, [], "Chinese without a glossary entry")

    def test_chinese_text_is_marked_lang_zh(self):
        problems = []
        for path in (os.path.join(ROOT, "index.html"), os.path.join(ROOT, "templates", "post.html")):
            checker = LangChecker()
            with open(path, encoding="utf-8") as f:
                checker.feed(f.read())
            problems += [f"{os.path.relpath(path, ROOT)}: {run}" for run in checker.unmarked]
        self.assertEqual(problems, [])

    def test_reduced_motion_rules_exist(self):
        with open(os.path.join(ROOT, "assets", "css", "style.css"), encoding="utf-8") as f:
            css = f.read()
        m = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", css, re.S)
        self.assertIsNotNone(m, "no prefers-reduced-motion: reduce block")
        for selector in (".petals", ".qa", ".talisman"):
            self.assertIn(selector, m.group(1))


if __name__ == "__main__":
    unittest.main()
