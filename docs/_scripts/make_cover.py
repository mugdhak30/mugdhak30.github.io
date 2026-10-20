"""Make a blog card cover from one of the post's photos.

Usage (run from the docs/ folder):

    python3 _scripts/make_cover.py Rio8
    python3 _scripts/make_cover.py Glacier2 --focus 0.78

Reads images/<name>.jpg and writes images/teasers/<name>.jpg: a 900x600 (3:2)
crop that stays above the bottom 12% of the photo, where the
"(c) Mugdha Khedkar" watermark sits.

--focus sets where the crop sits vertically in a tall (portrait) photo:
0 = top, 0.4 = slightly above the middle (default), 1 = as low as possible
without reaching the watermark. Landscape photos are always cropped from the
top 88% of the photo, centred left to right.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

WIDTH, HEIGHT = 900, 600
SAFE = 0.88  # keep the crop above the bottom 12% (watermark)


def main():
    parser = argparse.ArgumentParser(description="Make a 900x600 blog card cover.")
    parser.add_argument("name", help="photo name without .jpg, e.g. Rio8")
    parser.add_argument("--focus", type=float, default=0.4,
                        help="vertical crop position for portrait photos, 0 (top) to 1 (bottom)")
    args = parser.parse_args()

    src = Path("images") / f"{args.name}.jpg"
    if not src.exists():
        sys.exit(f"Not found: {src} (run this from the docs/ folder, without .jpg)")

    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    usable = int(h * SAFE)
    crop_h = min(usable, int(w * 2 / 3))
    crop_w = int(crop_h * 1.5)
    top = max(0, min(int((h - crop_h) * args.focus), usable - crop_h))
    left = (w - crop_w) // 2

    out = Path("images") / "teasers" / f"{args.name}.jpg"
    out.parent.mkdir(exist_ok=True)
    im.crop((left, top, left + crop_w, top + crop_h)).resize((WIDTH, HEIGHT), Image.LANCZOS) \
        .save(out, quality=80, optimize=True, progressive=True)
    print(f"Wrote {out}  (front matter:  teaser: /{out.as_posix()})")


if __name__ == "__main__":
    main()
