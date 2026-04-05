#!/usr/bin/env python3

import os
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path
import markdown

SITE_URL = "https://blog.rhysperry.com"
SITE_TITLE = "Rhys' Blog"
SITE_AUTHOR = "Rhys Perry"
POSTS_DIR = Path("posts")
OUT_DIR = Path("out")

STYLE = """<style>
  :root { color-scheme: dark light }
  body { max-width: 600px; margin: 2rem auto; padding: 0 1rem; font-family: monospace }
  a { color: inherit }
  nav { display: flex; gap: 1rem; margin-bottom: 2rem;}
  footer { margin-top: 3rem; opacity: 0.65;}
  .date { opacity: 0.65; }
  pre { overflow-x: auto; padding: 1rem; border: 1px solid; opacity: 0.8 }
  code { font-family: monospace }
  img { max-width: 100% }
</style>"""

NAV = """<nav>
  <a href="https://rhysperry.com">home</a>
  <a href="https://blog.rhysperry.com">blog</a>
  <a href="https://github.com/rhysperry111">github</a>
</nav>"""

FOOTER = """<footer>
  <a href="/feed.xml">rss</a>
</footer>"""


def parse_post(filepath):
    text = filepath.read_text()

    title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem

    date_match = re.search(r'^\*(\d{4}-\d{2}-\d{2})\*', text, re.MULTILINE)
    date_str = date_match.group(1) if date_match else "1970-01-01"
    date = datetime.strptime(date_str, "%Y-%m-%d")

    if date_match:
        body = text[date_match.end():].strip()
    elif title_match:
        body = text[title_match.end():].strip()
    else:
        body = text

    html = markdown.markdown(body, extensions=["fenced_code", "tables"])
    slug = filepath.stem

    return {
        "title": title,
        "date": date,
        "date_str": date_str,
        "slug": slug,
        "html": html,
    }


def render_post(post):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="author" content="{SITE_AUTHOR}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="alternate" type="application/rss+xml" title="Rhys' Blog" href="https://blog.rhysperry.com/feed.xml" />
<title>{post['title']} - {SITE_TITLE}</title>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{post['title']}",
  "author": {{
    "@type": "Person",
    "name": "Rhys Perry",
    "url": "https://rhysperry.com"
  }},
  "publisher": {{
    "@type": "Person",
    "name": "Rhys Perry"
  }},
  "datePublished": "{post['date_str']}"
}}
</script>
{STYLE}
</head>
<body>
{NAV}
<article>
<h1>{post['title']}</h1>
<p class="date">{post['date_str']}</p>
{post['html']}
</article>
{FOOTER}
</body>
</html>"""


def render_index(posts):
    items = ""
    for p in posts:
        items += f'<li>{p["date_str"]} — <a href="{SITE_URL}/{p["slug"]}/">{p["title"]}</a></li>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="author" content="{SITE_AUTHOR}">
<meta name="description" content="Rhys' Blog. Write-ups of things I've been doing and what I've been thinking about. Infrastructure/Network/GitOps/Cyber.">
<link rel="alternate" type="application/rss+xml" title="Rhys' Blog" href="https://blog.rhysperry.com/feed.xml" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "Rhys' Blog",
  "url": "https://blog.rhysperry.com/",
  "description": "Rhys' Blog. Write-ups of things I've been doing and what I've been thinking about. Infrastructure/Network/GitOps/Cyber.",
  "author": {{
    "@type": "Person",
    "name": "Rhys Perry",
    "url": "https://rhysperry.com"
  }},
  "publisher": {{
    "@type": "Person",
    "name": "Rhys Perry"
  }}
}}
</script>
<title>{SITE_TITLE}</title>
{STYLE}
</head>
<body>
{NAV}
<h1>Rhys' Blog</h1>
<ul>
{items}</ul>
{FOOTER}
</body>
</html>"""


def render_rss(posts):
    items = ""
    for p in posts[:20]:
        pub_date = p["date"].strftime("%a, %d %b %Y 00:00:00 GMT")
        # escape html for xml
        escaped = p["html"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        items += f"""    <item>
      <title>{p['title']}</title>
      <link>{SITE_URL}/{p['slug']}/</link>
      <guid>{SITE_URL}/{p['slug']}/</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{escaped}</description>
    </item>
"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}</link>
    <description>Rhys' Blog. Write-ups of things I've been doing and what I've been thinking about. Infrastructure/Network/GitOps/Cyber.</description>
{items}  </channel>
</rss>"""


def build():
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir()

    if not POSTS_DIR.exists():
        print("No posts/ directory found.")
        sys.exit(1)

    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        print("No .md files in posts/.")
        sys.exit(1)

    posts = [parse_post(f) for f in md_files]
    posts.sort(key=lambda p: p["date"], reverse=True)

    print(f"Found {len(posts)} posts:")

    for p in posts:
        post_dir = OUT_DIR / p["slug"]
        post_dir.mkdir()
        (post_dir / "index.html").write_text(render_post(p))
        print(f"  {p['date_str']}  {p['title']}")

    static_dir = Path("static")
    if static_dir.exists():
        shutil.copytree(static_dir, OUT_DIR / "static")

    robots_txt = Path("robots.txt")
    shutil.copyfile(robots_txt, OUT_DIR / "robots.txt")

    (OUT_DIR / "index.html").write_text(render_index(posts))

    (OUT_DIR / "feed.xml").write_text(render_rss(posts))

    print(f"\nDone. Output in {OUT_DIR}/")


if __name__ == "__main__":
    build()
