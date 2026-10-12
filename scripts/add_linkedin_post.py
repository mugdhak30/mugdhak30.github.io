#!/usr/bin/env python3
"""Feature a LinkedIn post in the home page's "Highlights from LinkedIn" cards.

Usage: python3 scripts/add_linkedin_post.py <link to a public LinkedIn post>

Reads the post's public page (no login needed), saves its first photo under
docs/assets/linkedin/, and adds the post to the top of docs/_data/linkedin.yml.
The home page shows the first SHOWN posts in that file; to unfeature a post,
delete its entry. Photos no longer used by any entry are deleted.
"""

import html
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
DATA = DOCS / "_data" / "linkedin.yml"
IMAGES = DOCS / "assets" / "linkedin"
SHOWN = 3  # keep in sync with `limit:` in docs/_includes/linkedin-posts.html
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def read_post(url):
    page = fetch(url).decode("utf-8", "replace")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    if not m:
        sys.exit("Could not read the post. Is it public, and is the link a post "
                 "(not a profile)? LinkedIn may also be blocking this network.")
    data = json.loads(m.group(1))
    if data.get("@type") != "SocialMediaPosting" or not data.get("articleBody"):
        sys.exit("The link does not look like a LinkedIn post.")
    images = [i["url"] for i in data.get("image", []) if isinstance(i, dict) and i.get("url")]
    return {
        "url": data.get("@id") or url.split("?")[0],
        "date": datetime.fromisoformat(data["datePublished"].replace("Z", "+00:00")),
        "text": html.unescape(data["articleBody"]).strip(),
        "image": images[0] if images else None,
    }


def post_id(url):
    m = re.search(r"(?:activity|share|ugcPost)[-:](\d{15,})", url)
    return m.group(1) if m else re.sub(r"\W+", "-", url)[-40:]


def split_entries(text):
    """Split the YAML list into (header comments, [entry blocks])."""
    parts = re.split(r"(?m)^(?=- )", text)
    return parts[0], parts[1:]


def entry_block(post, image_path):
    # A line starting with '#' would turn into a heading when rendered.
    body = "\n".join(("\\" + l if l.startswith("#") else l) for l in post["text"].splitlines())
    lines = [f"- date: {post['date']:%Y-%m-%d}", f"  url: {post['url']}"]
    if image_path:
        lines.append(f"  image: {image_path}")
    lines.append("  text: |")
    lines += [("    " + l) if l.strip() else "" for l in body.splitlines()]
    return "\n".join(lines)


def remove_unused_images(data_text):
    for f in IMAGES.glob("*"):
        if f"/assets/linkedin/{f.name}" not in data_text:
            f.unlink()


def main():
    if len(sys.argv) != 2 or "linkedin.com" not in sys.argv[1]:
        sys.exit(__doc__)
    post = read_post(sys.argv[1].strip())
    pid = post_id(post["url"])

    header, entries = split_entries(DATA.read_text(encoding="utf-8") if DATA.exists() else "")
    if any(pid in e for e in entries):
        sys.exit(f"Already on the site: {post['url']}")

    image_path = None
    if post["image"]:
        IMAGES.mkdir(parents=True, exist_ok=True)
        (IMAGES / f"{pid}.jpg").write_bytes(fetch(post["image"]))
        image_path = f"/assets/linkedin/{pid}.jpg"

    entries = [entry_block(post, image_path)] + [e.strip() for e in entries]
    text = header + "\n\n".join(entries) + "\n"
    DATA.write_text(text, encoding="utf-8")
    remove_unused_images(text)

    print(f"Featured {post['date']:%d %b %Y} post: {post['text'][:70]}...")
    for e in entries[SHOWN:]:
        url = re.search(r"^  url: (\S+)", e, re.M)
        print(f"Not shown (only the first {SHOWN} are), delete its entry if no longer wanted: "
              f"{url.group(1) if url else e.splitlines()[0]}")


if __name__ == "__main__":
    main()
