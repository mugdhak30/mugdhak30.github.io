"""Shrink a post's photos to the size the blog actually shows them at.

Usage (run from the docs/ folder):

    python3 _scripts/resize_photos.py _posts/2026-11-15-Pacific-Northwest.md
    python3 _scripts/resize_photos.py _posts/*.md --dry-run

For every photo in images/ that the given post(s) use, it finds the widest
size the photo is shown at anywhere on the site ({:width="400"} in a post),
and resizes it to twice that width, never below 1200 px. Twice the width keeps
photos sharp on phones and Retina screens, which use 2 device pixels per page
pixel. Nothing is cropped (the watermark stays) and file names do not change.

Photos that are already small enough, PNGs and the covers in images/teasers/
are left alone. Location data (GPS) and other camera metadata are removed.

It then adds each photo's height next to its width in the post(s),
{:width="400" height="889" ...}, so the browser keeps the photo's space free
while it loads and the text doesn't jump. Running it again changes nothing.
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

MIN_WIDTH = 1200      # never smaller than this, so a photo can later be shown larger
DEFAULT_SHOWN = 850   # a photo without a width is shown at most this wide
QUALITY = 88

# Only the site's own photos: "(/images/..." or "\"/images/...", not links like https://other.site/images/...
IMAGE = re.compile(r'(?<=[("\'])/images/([^)\s"\']+\.jpe?g)\)?(?:\{:\s*width="(\d+)")?', re.I)
PAGES = ["_posts/*.md", "_drafts/*.md", "_pages/*.md", "_pages/*.html", "*.md", "year-archive/*.html"]
# A photo in a post with its attributes: ![...](/images/name.jpg){:width="400" style="..."}
PHOTO_ATTRS = re.compile(r'(\]\(/images/([^)\s]+\.jpe?g)\)\{:)([^}]*)\}', re.I)
# A photo without any: ![...](/images/name.jpg)
PHOTO_BARE = re.compile(r'(\]\(/images/([^)\s]+\.jpe?g)\))(?!\{)', re.I)


def shown_widths():
    """Widest size each photo is shown at, across every post and page."""
    widths = {}
    for pattern in PAGES:
        for page in Path(".").glob(pattern):
            for name, width in IMAGE.findall(page.read_text(encoding="utf-8")):
                w = int(width) if width else DEFAULT_SHOWN
                widths[name] = max(widths.get(name, 0), w)
    return widths


def add_heights(post, dry_run):
    """Write height="..." next to width="..." for each photo in the post. Returns how many were added."""
    sizes = {}

    def with_height(m):
        attrs = m.group(3)
        width = re.search(r'width="(\d+)"', attrs)
        path = Path("images") / m.group(2)
        if not width or "height=" in attrs or not path.exists():
            return m.group(0)
        if path not in sizes:
            sizes[path] = ImageOps.exif_transpose(Image.open(path)).size
        w, h = sizes[path]
        height = round(int(width.group(1)) * h / w)
        return m.group(1) + attrs.replace(width.group(0), f'{width.group(0)} height="{height}"', 1) + "}"

    def with_size(m):
        # No width given: the photo is shown at its own size, shrunk to fit the column,
        # so its own pixel size is the width and height that keep it looking the same
        path = Path("images") / m.group(2)
        if not path.exists():
            return m.group(0)
        w, h = ImageOps.exif_transpose(Image.open(path)).size
        return f'{m.group(1)}{{:width="{w}" height="{h}"}}'

    text = Path(post).read_text(encoding="utf-8")
    new = PHOTO_ATTRS.sub(with_height, text)
    added = sum(1 for a, b in zip(PHOTO_ATTRS.findall(text), PHOTO_ATTRS.findall(new)) if a != b)
    new, bare = PHOTO_BARE.subn(with_size, new)
    added += bare
    if added and not dry_run:
        Path(post).write_text(new, encoding="utf-8")
    return added


def main():
    parser = argparse.ArgumentParser(description="Shrink a post's photos to the size the blog shows them at.")
    parser.add_argument("posts", nargs="+", help="post files, e.g. _posts/2025-02-23-Zermatt.md")
    parser.add_argument("--dry-run", action="store_true", help="only report what would change")
    args = parser.parse_args()

    if not Path("images").is_dir():
        sys.exit("Run this from the docs/ folder.")
    widths = shown_widths()

    names = []
    for post in args.posts:
        for name, _ in IMAGE.findall(Path(post).read_text(encoding="utf-8")):
            if not name.startswith("teasers/") and name not in names:
                names.append(name)

    before = after = 0
    for name in names:
        path = Path("images") / name
        if not path.exists():
            print(f"  missing   {name}")
            continue
        size = path.stat().st_size
        im = ImageOps.exif_transpose(Image.open(path))
        target = max(2 * widths.get(name, DEFAULT_SHOWN), MIN_WIDTH)
        before += size
        if im.width <= target:
            after += size
            print(f"  ok        {name:28} {im.width}x{im.height}, already small enough")
            continue
        height = round(im.height * target / im.width)
        if not args.dry_run:
            icc = im.info.get("icc_profile")
            im.convert("RGB").resize((target, height), Image.LANCZOS).save(
                path, "JPEG", quality=QUALITY, optimize=True, progressive=True,
                **({"icc_profile": icc} if icc else {}))
            new = path.stat().st_size
        else:
            new = size  # unknown until saved
        after += new
        print(f"  resized   {name:28} {im.width}x{im.height} -> {target}x{height}"
              f"   {size / 1e6:4.1f} MB -> {new / 1e6:4.2f} MB")

    if not args.dry_run:
        print(f"\n{len(names)} photos: {before / 1e6:.0f} MB -> {after / 1e6:.0f} MB")

    heights = sum(add_heights(post, args.dry_run) for post in args.posts)
    print(f"Heights {'to add' if args.dry_run else 'added'}: {heights}")


if __name__ == "__main__":
    main()
