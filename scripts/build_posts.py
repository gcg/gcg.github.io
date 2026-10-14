#!/usr/bin/env python3
"""
Zero-dependency static blog article generator for gcg.github.io.
Compiles markdown files in content/posts/ into standalone HTML pages
at posts/<slug>/index.html and syncs Chapter 04 chronicle cards in index.html.
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

    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()

            # Strip quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]

            # Parse booleans
            if val.lower() == "true":
                meta[key] = True
            elif val.lower() == "false":
                meta[key] = False
            # Parse inline lists like ["tag1", "tag2"]
            elif val.startswith("[") and val.endswith("]"):
                items = [re.sub(r"^['\"]|['\"]$", "", item.strip()) for item in val[1:-1].split(",") if item.strip()]
                meta[key] = items
            else:
                meta[key] = val

    return meta, body


def format_date(iso_str):
    """Converts ISO timestamp into readable string (e.g. February 1, 2024)."""
    if not iso_str:
        return "Recent Archive"
    clean_str = str(iso_str).split("T")[0]
    try:
        dt = datetime.strptime(clean_str, "%Y-%m-%d")
        return dt.strftime("%B %-d, %Y")
    except Exception:
        return clean_str


def estimate_reading_time(text):
    """Calculates reading time in minutes."""
    words = len(re.findall(r"\w+", text))
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def extract_excerpt(text):
    """Extracts a short plaintext summary from the markdown body."""
    # Strip markdown elements
    clean = re.sub(r"```[\s\S]*?```", "", text)
    clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
    clean = re.sub(r"[#*_>`]", "", clean)
    for para in clean.split("\n\n"):
        para = para.strip().replace("\n", " ")
        if len(para) > 30:
            if len(para) > 180:
                return para[:177].rsplit(" ", 1)[0] + "..."
            return para
    return "Hunter system record from the personal chronicles."


def slugify(text):
    """Generates an HTML ID safe slug."""
    s = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", s)


def markdown_to_html(md_text):
    """Converts standard Markdown into semantic HTML."""
    code_blocks = []

    def save_code_block(match):
        lang = match.group(1).strip()
        code_content = match.group(2)
        escaped_code = html.escape(code_content)
        cls = f' class="language-{lang}"' if lang else ""
        idx = len(code_blocks)
        code_blocks.append(f"<pre><code{cls}>{escaped_code}</code></pre>")
        return f"\n__CODE_BLOCK_{idx}__\n"

    # 1. Preserve fenced code blocks
    text = re.sub(r"```([a-zA-Z0-9_-]*)\n(.*?)\n```", save_code_block, md_text, flags=re.DOTALL)

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

    # 6. Process line-by-line / block-by-block
    lines = text.split("\n")
    output_lines = []
    in_ul = False
    in_ol = False
    in_blockquote = False

    for line in lines:
        stripped = line.strip()

        # Check blockquote
        if stripped.startswith("> "):
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
            if not in_ol:
                output_lines.append("<ol>")
                in_ol = True
            output_lines.append(f"<li>{ol_match.group(1).strip()}</li>")
            continue
        elif in_ol:
            output_lines.append("</ol>")
            in_ol = False

        # Headings
        if stripped.startswith("#### "):
            h_text = stripped[5:].strip()
            output_lines.append(f'<h5 id="{slugify(h_text)}">{h_text}</h5>')
        elif stripped.startswith("### "):
            h_text = stripped[4:].strip()
            output_lines.append(f'<h4 id="{slugify(h_text)}">{h_text}</h4>')
        elif stripped.startswith("## "):
            h_text = stripped[3:].strip()
            output_lines.append(f'<h3 id="{slugify(h_text)}">{h_text}</h3>')
        elif stripped.startswith("# "):
            h_text = stripped[2:].strip()
            output_lines.append(f'<h2 id="{slugify(h_text)}">{h_text}</h2>')
        elif stripped.startswith("__CODE_BLOCK_"):
            output_lines.append(stripped)
        elif stripped == "":
            output_lines.append("")
        else:
            output_lines.append(f"<p>{stripped}</p>")

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

        # Skip drafts
        if meta.get("draft") is True:
            print(f"Skipping draft: {slug}")
            continue

        title = meta.get("title", slug)
        date_raw = meta.get("date", "")
        formatted_date = format_date(date_raw)
        reading_time = estimate_reading_time(body_md)
        excerpt = extract_excerpt(body_md)
        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        tags_html = "".join([f'<span class="tag-pill">#{t}</span>' for t in tags])
        body_html = markdown_to_html(body_md)

        # Create output dir
        post_out_dir = os.path.join(OUTPUT_DIR, slug)
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


def sync_homepage(posts):
    """Updates Chapter 04 in index.html with synced chronicle cards."""
    if not os.path.isfile(HOMEPAGE_PATH):
        return

    with open(HOMEPAGE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- CHRONICLES_START -->"
    end_tag = "<!-- CHRONICLES_END -->"

    if start_tag not in content or end_tag not in content:
        # Markers will be added in Task 4
        return

    cards = []
    for p in posts:
        slug = p["slug"]
        card = f"""        <!-- Chronicle: {p['title']} -->
        <article class="chronicle-card">
          <header class="chronicle-header">
            <div class="chronicle-meta">
              <span class="chronicle-date">{p['formatted_date']}</span>
              <div class="chronicle-tags">
                {p['tags_html']}
              </div>
            </div>
            <a href="posts/{slug}/" style="text-decoration: none;">
              <h3 class="chronicle-title" style="transition: color 0.2s ease;">{p['title']}</h3>
            </a>
            <p class="chronicle-excerpt">
              {p['excerpt']}
            </p>
          </header>

          <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.5rem;">
            <button class="chronicle-toggle-btn" type="button" aria-expanded="false" data-target="chronicle-{slug}">
              <span>Preview Chronicle</span>
              <span class="toggle-icon">▾</span>
            </button>
            <a href="posts/{slug}/" class="chronicle-toggle-btn" style="text-decoration: none; border-color: rgba(0, 229, 255, 0.4);" title="Open full chronicle on dedicated page">
              <span>Open Full Chronicle</span>
              <span>↗</span>
            </a>
          </div>

          <!-- Inline Preview Container -->
          <div id="chronicle-{slug}" class="chronicle-content" aria-hidden="true">
            <div class="chronicle-prose">
              {p['body_html']}
            </div>
          </div>
        </article>"""
        cards.append(card)

    cards_html = "\n\n".join(cards)
    pattern = re.compile(rf"{re.escape(start_tag)}[\s\S]*?{re.escape(end_tag)}")
    new_content = pattern.sub(f"{start_tag}\n{cards_html}\n        {end_tag}", content)

    with open(HOMEPAGE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Homepage Chapter 04 synchronized with generated chronicles.")


def main():
    print("Building standalone articles...")
    posts = build_posts()
    sync_homepage(posts)
    print(f"Successfully processed {len(posts)} articles.")


if __name__ == "__main__":
    main()
