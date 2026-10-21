#!/usr/bin/env python3
"""
Zero-dependency static blog article generator for gcg.github.io.
Compiles markdown files in content/posts/ into standalone HTML pages
at posts/<slug>/index.html and syncs the Scripture Pavilion list in index.html.
"""

import os
import sys
import re
import shutil
import html
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT_DIR, "content", "posts")
OUTPUT_DIR = os.path.join(ROOT_DIR, "posts")
TEMPLATE_PATH = os.path.join(ROOT_DIR, "templates", "post.html")
HOMEPAGE_PATH = os.path.join(ROOT_DIR, "index.html")


def parse_frontmatter(raw_content):
    """Extracts YAML frontmatter and markdown body."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw_content, re.DOTALL)
    if not match:
        return {}, raw_content

    fm_text = match.group(1)
    body = match.group(2)
    meta = {}
    current_key = None
    multiline_buf = []

    def commit_key(key, lines):
        if not key or not lines:
            return
        combined = " ".join(l.strip() for l in lines).strip()
        val_clean = re.sub(r"^['\"]|['\"]$", "", combined).strip()

        # Parse booleans
        if val_clean.lower() in ("true", "yes", "1"):
            meta[key] = True
        elif val_clean.lower() in ("false", "no", "0"):
            meta[key] = False
        # Parse inline list: ["a", "b"]
        elif combined.startswith("[") and combined.endswith("]"):
            items = [re.sub(r"^['\"]|['\"]$", "", item.strip()) for item in combined[1:-1].split(",") if item.strip()]
            meta[key] = items
        # Parse YAML bullet list
        elif any(l.strip().startswith("- ") for l in lines):
            items = [re.sub(r"^['\"]|['\"]$", "", l.strip()[2:].strip()) for l in lines if l.strip().startswith("- ")]
            meta[key] = items
        else:
            meta[key] = val_clean

    for line in fm_text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key_match = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if key_match:
            if current_key:
                commit_key(current_key, multiline_buf)
            current_key = key_match.group(1).strip()
            rest = key_match.group(2).strip()
            multiline_buf = [rest] if rest else []
        else:
            if current_key:
                multiline_buf.append(line.strip())

    if current_key:
        commit_key(current_key, multiline_buf)

    return meta, body


def format_date(iso_str):
    """Converts ISO timestamp into readable string (e.g. February 1, 2024). Platform independent."""
    if not iso_str:
        return "Recent Archive"
    clean_str = str(iso_str).split("T")[0]
    try:
        dt = datetime.strptime(clean_str, "%Y-%m-%d")
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}"
    except Exception:
        return clean_str


def estimate_reading_time(text):
    """Calculates reading time in minutes."""
    words = len(re.findall(r"\w+", text))
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def extract_excerpt(text):
    """Extracts a short plaintext summary from the markdown body."""
    clean = re.sub(r"```[\s\S]*?```", "", text)
    clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
    clean = re.sub(r"[#*_>`]", "", clean)
    for para in clean.split("\n\n"):
        para = para.strip().replace("\n", " ")
        if len(para) > 30:
            if len(para) > 180:
                return para[:177].rsplit(" ", 1)[0] + "..."
            return para
    return "A scroll from the Scripture Pavilion of gcg.me."


def slugify(text):
    """Generates an HTML ID safe slug."""
    s = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", s)


def markdown_to_html(md_text):
    """Converts standard Markdown into semantic HTML."""
    # Normalize line endings
    md_text = md_text.replace("\r\n", "\n").replace("\r", "\n")

    code_blocks = []

    def save_code_block(match):
        lang = match.group(1).strip()
        code_content = match.group(2)
        escaped_code = html.escape(code_content)
        cls = f' class="language-{lang}"' if lang else ""
        idx = len(code_blocks)
        code_blocks.append(f"<pre><code{cls}>{escaped_code}</code></pre>")
        return f"\n__CODE_BLOCK_{idx}__\n"

    # 1. Preserve fenced code blocks (handling trailing spaces, tabs, and languages like c++, c#)
    text = re.sub(r"```([a-zA-Z0-9_+\#-]*)[ \t]*\n(.*?)\n[ \t]*```", save_code_block, md_text, flags=re.DOTALL)

    # 2. Linked images: [![alt](src)](url)
    text = re.sub(
        r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)",
        r'<a href="\3" target="_blank" rel="noopener noreferrer"><img src="\2" alt="\1" loading="lazy"></a>',
        text
    )

    # 3. Images: ![alt](src)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        r'<figure><img src="\2" alt="\1" loading="lazy"><figcaption>\1</figcaption></figure>',
        text
    )

    # 4. Links: [text](url)
    def format_link(match):
        label = match.group(1)
        url = match.group(2)
        if url.startswith("http://") or url.startswith("https://"):
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'
        return f'<a href="{url}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", format_link, text)

    # 5. Inline code, bold, italics
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    # 6. Process line-by-line / block-by-block with paragraph accumulation
    lines = text.split("\n")
    output_lines = []
    in_ul = False
    in_ol = False
    in_blockquote = False
    para_buf = []

    def flush_para():
        if para_buf:
            joined = " ".join(para_buf).strip()
            if joined:
                output_lines.append(f"<p>{joined}</p>")
            para_buf.clear()

    for line in lines:
        stripped = line.strip()

        # Check blockquote
        if stripped.startswith("> "):
            flush_para()
            if not in_blockquote:
                output_lines.append("<blockquote>")
                in_blockquote = True
            output_lines.append(f"<p>{stripped[2:].strip()}</p>")
            continue
        elif in_blockquote:
            output_lines.append("</blockquote>")
            in_blockquote = False

        # Check unordered list
        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_para()
            if not in_ul:
                output_lines.append("<ul>")
                in_ul = True
            item_text = stripped[2:].strip()
            output_lines.append(f"<li>{item_text}</li>")
            continue
        elif in_ul:
            output_lines.append("</ul>")
            in_ul = False

        # Check ordered list
        ol_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ol_match:
            flush_para()
            if not in_ol:
                output_lines.append("<ol>")
                in_ol = True
            output_lines.append(f"<li>{ol_match.group(1).strip()}</li>")
            continue
        elif in_ol:
            output_lines.append("</ol>")
            in_ol = False

        # Headings (escaped content)
        if stripped.startswith("#### "):
            flush_para()
            h_text = stripped[5:].strip()
            output_lines.append(f'<h5 id="{slugify(h_text)}">{html.escape(h_text)}</h5>')
        elif stripped.startswith("### "):
            flush_para()
            h_text = stripped[4:].strip()
            output_lines.append(f'<h4 id="{slugify(h_text)}">{html.escape(h_text)}</h4>')
        elif stripped.startswith("## "):
            flush_para()
            h_text = stripped[3:].strip()
            output_lines.append(f'<h3 id="{slugify(h_text)}">{html.escape(h_text)}</h3>')
        elif stripped.startswith("# "):
            flush_para()
            h_text = stripped[2:].strip()
            output_lines.append(f'<h2 id="{slugify(h_text)}">{html.escape(h_text)}</h2>')
        elif stripped.startswith("__CODE_BLOCK_"):
            flush_para()
            output_lines.append(stripped)
        elif stripped == "":
            flush_para()
            output_lines.append("")
        else:
            para_buf.append(stripped)

    flush_para()
    if in_ul:
        output_lines.append("</ul>")
    if in_ol:
        output_lines.append("</ol>")
    if in_blockquote:
        output_lines.append("</blockquote>")

    result_html = "\n".join(output_lines)

    # 7. Restore code blocks
    for i, cb in enumerate(code_blocks):
        result_html = result_html.replace(f"<p>__CODE_BLOCK_{i}__</p>", cb)
        result_html = result_html.replace(f"__CODE_BLOCK_{i}__", cb)

    # Clean empty paragraphs
    result_html = re.sub(r"<p>\s*</p>", "", result_html)
    return result_html


def build_posts():
    """Builds all posts from content/posts/ to posts/<slug>/index.html."""
    if not os.path.isdir(CONTENT_DIR):
        print(f"Content directory not found: {CONTENT_DIR}")
        return []

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    posts = []

    for entry in sorted(os.listdir(CONTENT_DIR)):
        entry_path = os.path.join(CONTENT_DIR, entry)
        slug = entry
        md_file = None

        if os.path.isdir(entry_path):
            index_path = os.path.join(entry_path, "index.md")
            if os.path.isfile(index_path):
                md_file = index_path
        elif entry.endswith(".md"):
            slug = entry[:-3]
            md_file = entry_path

        if not md_file:
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            raw_content = f.read()

        meta, body_md = parse_frontmatter(raw_content)

        post_out_dir = os.path.join(OUTPUT_DIR, slug)

        # Skip and prune drafts
        is_draft = str(meta.get("draft", "")).strip("'\"").lower() in ("true", "yes", "1")
        if is_draft:
            print(f"Skipping draft: {slug}")
            if os.path.isdir(post_out_dir):
                shutil.rmtree(post_out_dir, ignore_errors=True)
            continue

        title = meta.get("title", slug)
        date_raw = meta.get("date", "")
        formatted_date = format_date(date_raw)
        reading_time = estimate_reading_time(body_md)
        excerpt = extract_excerpt(body_md)
        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        tags_html = "".join([f'<span class="tag-pill">#{html.escape(t)}</span>' for t in tags])
        body_html = markdown_to_html(body_md)

        # Create output dir
        os.makedirs(post_out_dir, exist_ok=True)

        # Copy sibling assets (e.g. images) if entry was a directory
        if os.path.isdir(entry_path):
            for file_name in os.listdir(entry_path):
                if file_name != "index.md" and not file_name.startswith("."):
                    src_file = os.path.join(entry_path, file_name)
                    dst_file = os.path.join(post_out_dir, file_name)
                    if os.path.isfile(src_file):
                        shutil.copy2(src_file, dst_file)

        # Render template
        page_html = template
        page_html = page_html.replace("{{title}}", html.escape(title))
        page_html = page_html.replace("{{slug}}", html.escape(slug))
        page_html = page_html.replace("{{formatted_date}}", html.escape(formatted_date))
        page_html = page_html.replace("{{date}}", str(date_raw))
        page_html = page_html.replace("{{reading_time}}", html.escape(reading_time))
        page_html = page_html.replace("{{excerpt}}", html.escape(excerpt))
        page_html = page_html.replace("{{tags_html}}", tags_html)
        page_html = page_html.replace("{{content}}", body_html)

        out_file = os.path.join(post_out_dir, "index.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"Generated: posts/{slug}/index.html")

        posts.append({
            "slug": slug,
            "title": title,
            "date": date_raw,
            "formatted_date": formatted_date,
            "reading_time": reading_time,
            "tags": tags,
            "tags_html": tags_html,
            "excerpt": excerpt,
            "body_html": body_html
        })

    # Sort posts descending by date
    posts.sort(key=lambda p: str(p.get("date", "")), reverse=True)
    return posts


def post_year(date_raw):
    """Returns the four-digit year of an ISO date string, or "" if there is none."""
    m = re.match(r"^(\d{4})-\d{2}-\d{2}", str(date_raw or ""))
    return m.group(1) if m else ""


def render_pavilion(posts):
    """Renders one Scripture Pavilion row per post, in the given order."""
    return "\n".join(
        f'<li class="scroll-row"><a href="posts/{p["slug"]}/">{html.escape(p["title"])}</a>'
        f'<span class="scroll-year">{post_year(p.get("date"))}</span></li>'
        for p in posts
    )


def sync_homepage(posts, homepage_path=HOMEPAGE_PATH):
    """Refills the Scripture Pavilion list between the markers. Returns False if the markers are missing."""
    if not os.path.isfile(homepage_path):
        return False

    with open(homepage_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- CHRONICLES_START -->"
    end_tag = "<!-- CHRONICLES_END -->"
    if start_tag not in content or end_tag not in content:
        return False

    pattern = re.compile(rf"{re.escape(start_tag)}[\s\S]*?{re.escape(end_tag)}")
    rows = render_pavilion(posts)
    new_content = pattern.sub(lambda _: f"{start_tag}\n{rows}\n{end_tag}", content, count=1)

    with open(homepage_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Scripture Pavilion synchronized with generated posts.")
    return True


def main():
    print("Building standalone articles...")
    posts = build_posts()
    sync_homepage(posts)
    print(f"Successfully processed {len(posts)} articles.")


if __name__ == "__main__":
    main()
