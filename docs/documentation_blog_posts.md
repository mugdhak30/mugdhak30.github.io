# Publishing a new blog post

Every travel post appears in two places: as its own page, and as a card on the blog index (`/year-archive/`). The card shows a cover photo, the country, the month and year, the title and a one-line teaser. All of this comes from the post's front matter, so a new post needs no changes anywhere else.

| Step | What you do |
|---|---|
| 1. Write | Create `_posts/YYYY-MM-DD-Short-Title.md` (or start in `_drafts/`) |
| 2. Photos | Put the photos in `images/` and add them to the post |
| 3. Shrink | Run `python3 _scripts/resize_photos.py _posts/YYYY-MM-DD-Short-Title.md` |
| 4. Cover | Run `python3 _scripts/make_cover.py PhotoName` |
| 5. Front matter | Fill in `title`, `tags`, `description` and `header.teaser` |
| 6. Check | Preview locally, then commit and push |

`year-archive/index.html`, `_includes/post-card.html` and `_sass/custom.scss` never need to change for a new post.

---

## 1. Create the file

Posts live in `_posts/`, one file per post, named with the date and a short title:

```
_posts/2026-11-15-Pacific-Northwest.md
```

- **The date** decides the year group on the blog index and the "November 2026" on the card.
- **The part after the date** becomes the address: `mugdhak30.github.io/Pacific-Northwest/`. Use hyphens, no spaces, and don't change it after publishing, or old links break.

**Not ready to publish?** Put the file in `_drafts/` instead, without a date in the name, e.g. `_drafts/Pacific-Northwest.md`. Drafts don't appear on the site. Preview them with `bundle exec jekyll serve --drafts`, and move the file into `_posts/` with a date when it's finished.

Never leave unfinished posts in the `docs/` root: Jekyll publishes every page there.

## 2. Add the photos

Put the photos in `images/`, named after the place and numbered: `PacificNW1.jpg`, `PacificNW2.jpg`, … Add them straight from your phone; step 3 shrinks them.

In the post, photos go inside a centred block. Use `width="400"` for photos side by side and `width="750"` for a single wide one:

```markdown
{:refdef: style="text-align: center;"}
![](/images/PacificNW1.jpg){:width="400" style="padding:20px"}
![](/images/PacificNW2.jpg){:width="400" style="padding:20px"}
{:refdef}
{:refdef: style="text-align: center;"}
*Left to Right: Whidbey Island and the ferry to Seattle*
{: refdef}
```

The second block is an optional caption in italics.

## 3. Shrink the photos

Once the post's text and photo widths are final, run this from the `docs/` folder:

```bash
python3 _scripts/resize_photos.py _posts/2026-11-15-Pacific-Northwest.md
```

It prints each photo's size before and after, e.g. `5.8 MB -> 0.54 MB`.

**Why:** phone photos are 4000+ px wide and 5–8 MB each, but the post shows them 400 or 750 px wide, and visitors download every one in full. GitHub Pages also allows a site of at most 1 GB, and full-size photos are what pushed this site past 4 GB, which makes deploys time out.

**What it does:** for each photo the post uses, it finds the widest `width="…"` it is shown at anywhere on the site and resizes it to twice that (never below 1200 px). Twice the width is what phones and Retina screens need to look sharp, so the post looks the same as with the originals. A 400 px photo becomes 1200 px wide, a 750 px panorama 1500 px.

- Nothing is cropped (the watermark stays) and file names don't change, so the post needs no edits.
- Photos that are already small enough, and the covers in `images/teasers/`, are left alone. Running it twice is harmless.
- It removes camera metadata, including the GPS location phones store in each photo.
- Add `--dry-run` to see what it would do without changing anything.

**Run it after the widths are final.** It reads them from the post. If you later show a shrunk photo larger (`width="400"` → `width="750"`), it will look slightly soft on Retina screens: copy the original back into `images/` and run the script again.

**Keep your originals elsewhere** (phone, Google Photos, a drive). The repository only keeps the smaller copies.

## 4. Make the cover

Pick the photo you want on the card, then run this from the `docs/` folder, giving the name without `.jpg`:

```bash
python3 _scripts/make_cover.py PacificNW3
```

This writes `images/teasers/PacificNW3.jpg`, a 900×600 crop (about 100 KB) that the card shows. It always stops above the bottom 12% of the photo, so the "© Mugdha Khedkar" watermark never appears half cut off on the card.

**Choosing a cover photo:**

- **Landscape photos work best.** The crop keeps their full height and trims a little from each side, so the cover looks almost like the original.
- **Portrait photos lose most of their height.** Only a band across the middle is kept, so they work when the subject sits slightly above the middle (a statue, a tower top, a person).
- **If a portrait crop misses the subject,** move the band with `--focus`, from `0` (top) to `1` (as low as it can go above the watermark). The default is `0.4`:

  ```bash
  python3 _scripts/make_cover.py Glacier2 --focus 0.78
  ```

Open the result in `images/teasers/` and run it again with a different `--focus` until the subject is in frame.

**Changing a cover later:** make the new one, point `header.teaser` at it, and delete the old file from `images/teasers/` so the folder holds only covers that are in use.

## 5. Fill in the front matter

The block between the `---` lines at the top of the post:

```yaml
---
layout: archive
title:  "Pacific Northwest: Islands and Evergreens"
author_profile: true
tags: USA
description: "A reunion in Seattle, ferries between islands, and forests that stay green all winter."
header:
  teaser: /images/teasers/PacificNW3.jpg
---
```

| Field | Required | Notes |
|---|---|---|
| `layout` | yes | Always `archive`. |
| `title` | yes | Shown on the post and on the card. |
| `author_profile` | yes | Always `true`: shows your profile next to the post. |
| `tags` | yes | The country, in capitals on the card (`USA`, `Germany`). Use one country per post. It also groups the post on `/blogs_by_country/`. Write a name with a space as a list, `tags: ["Czech Republic"]`, or Jekyll splits it into two tags. |
| `description` | yes | The one-line teaser on the card. See below. |
| `header.teaser` | yes | The cover from step 4. Indent `teaser:` by two spaces under `header:`. A post without one still appears, just without a photo. |

### Writing the description

The description does three jobs at once: it's the teaser on the card, the snippet under the post in Google, and the text in LinkedIn and WhatsApp link previews.

- **One sentence, at most about 115 characters.** The card shows three lines and cuts anything longer with "…".
- **Say what the post is about.** Your opening paragraph draws readers into the story; the description should tell them where you went and what happened. Two or three concrete details work well: *"Sedona's red rocks, a surprise snowstorm, and the observatory where Pluto was discovered."*
- **Write in your own voice,** first person is fine: *"My first trip to the Southern Hemisphere: Melbourne's trams, an untimely autumn and an upside-down moon."*
- **For two-part trips,** give each post different details so the cards don't repeat each other.
- **Use American spelling** ("canceled", "color"), to match the rest of the cards.
- **Wrap it in double quotes.** Apostrophes inside are fine; use single quotes for a quotation inside it: *"…on the 'slowest express train in the world'…"*

Without a description, the card falls back to the first sentence of the post, which is often a scene-setting line like "2026 has been exciting, to say the least."

## 6. Check and publish

Preview the site locally:

```bash
bundle exec jekyll serve
```

Then open:

- **`http://127.0.0.1:4000/year-archive/`**: the new card should be first under its year, with the cover, country, date, title and full description (no "…").
- **The post itself**, at `http://127.0.0.1:4000/Short-Title/`.

Commit the post, its photos in `images/` and its cover in `images/teasers/` together, then push.

---

## Checklist

- [ ] `_posts/YYYY-MM-DD-Short-Title.md` created (or moved out of `_drafts/`)
- [ ] Photos added to `images/` and shrunk with `_scripts/resize_photos.py`
- [ ] Cover made with `_scripts/make_cover.py` and checked
- [ ] Front matter has `title`, `tags`, `description` and `header.teaser`
- [ ] Description is one sentence and fits on the card without "…"
- [ ] Previewed on `/year-archive/` and on the post page
- [ ] Post, photos and cover committed together
