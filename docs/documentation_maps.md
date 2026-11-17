# Updating the maps

The site has two maps:

| Map | Where | Shows |
|---|---|---|
| Talks map | top of `/talks/`, above the list | talks given in person (`_data/talks.yml`), except thesis defences, and posters (`_data/posters.yml`) |
| Blog map | top of `/year-archive/` | blog posts with `places:` in their front matter |

Both are built from data files. The page colours the dots, shades the countries, fills in the panel that opens when a dot is clicked and updates the counters without any further edits.

| To add… | Edit |
|---|---|
| A place the maps don't know yet | `_data/places.yml` (always first, see [Step 1](#step-1-make-sure-the-place-exists)) |
| A talk you gave in person | `place:` on the talk's stop in `_data/talks.yml` |
| A poster | `_data/posters.yml` |
| A place you wrote a blog post about | `places:` in the post's front matter |

A place only appears on a map once a talk, poster or post points to it. There is no list of places you've been to but haven't written about: everything in this repository is public on GitHub, so keep such lists elsewhere.

---

## Step 1: Make sure the place exists

Every entry refers to a place by a short id, such as `lisbon` or `joshua-tree`. The id is defined once in `_data/places.yml` and reused everywhere. Search the file first: the place may already be there.

To add a place, add one line in the section for its country or region:

```yaml
abisko:         { name: "Abisko", cc: SE, lat: 68.349, lng: 18.831 }
```

| Field | Notes |
|---|---|
| id (before the `:`) | Lowercase, with hyphens instead of spaces: `san-francisco`, `mt-rainier`. Must be unique. |
| `name` | Shown when you hover over or click the dot. Keep the quotes. |
| `cc` | Two-letter country code in capitals: `IN`, `DE`, `US`. Decides which country is shaded and which flag is shown. |
| `lat`, `lng` | Decimal degrees. In Google Maps, right-click the spot and click the numbers at the top of the menu to copy them. South and west are negative: Rio is `lat: -22.906, lng: -43.173`. Three decimals are plenty. |

Add the place in the same commit as the talk, poster or post that uses it, not before.

### A new country

If `cc` is a country not yet in `_data/countries.yml`, add it there too:

```yaml
JP: { name: "Japan", flag: "🇯🇵" }
```

Without this line the place still appears, but without a flag or country name.

---

## Talks map

### A talk

Give the talk's stop in `_data/talks.yml` a `place:` (see `documentation_research_talks.md`):

```yaml
  stops:
    - venue: "Security Group, University of Tokyo"
      place: tokyo
      flag: 🇯🇵
      date: "2027-03"
```

For a talk given online, write `virtual: true` instead of `place:`. It stays in the list on `/talks/` but is left off the map. A stop with neither is also left off the map.

### A poster

Add an entry to `_data/posters.yml`:

```yaml
- place: melbourne
  date: "2023-05"
  what: "ICSE 2023 Doctoral Symposium"
```

`date` is `"YYYY-MM"`, or just `"YYYY"`. `what` is shown next to a Poster badge when the dot is clicked.

### Dot colours

Each dot takes the colour of the most recent talk given there, grouped by the talk's `badge`:

| Badge | Colour group |
|---|---|
| `pub-mobilesoft`, `pub-icse`, `pub-asew`, `pub-asejournal`, `workshop`, posters | Paper or poster at a conference or workshop |
| `invited-talk`, `industry-talk` | Invited or industry talk |

Thesis defences (any badge containing `defense`) are left off the map. A new badge falls into the first group until you add it to `GROUP` near the top of `assets/js/place-map.js`.

---

## Blog map

Add a `places:` line to the post's front matter, next to `tags:`:

```yaml
places: [seattle, mt-rainier]
```

- The square brackets are required, even for one place: `places: [lisbon]`.
- A post can have several places, and several posts can share a place. The panel lists posts oldest first.
- Leave `places:` out of posts that aren't about a trip.

---

## Check and publish

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/talks/` or `http://127.0.0.1:4000/year-archive/` and check that the dot appears, in the right colour, and that clicking it shows the right entries.

If a dot is missing, open the browser console (F12 → Console). An id missing from `_data/places.yml` produces a warning such as:

```
place-map: unknown place "tokio" (…); add it to _data/places.yml
```

---

## Changing the maps themselves

| To change… | Edit |
|---|---|
| The heading and text above a map | `_pages/talks.md` or `year-archive/index.html` |
| The legend and hint text | `_includes/place-map.html` |
| Where each map is centred and zoomed | `VIEW` near the top of `assets/js/place-map.js` |
| Colours (light and dark theme) | the `.place-map` block at the end of `_sass/custom.scss` |

The talks map is shorter than the blog map (3:1, set in `_sass/custom.scss`) and cropped to the area with talks (California to Melbourne, up to Copenhagen), checked at phone and desktop widths. If you present somewhere outside it, loosen `VIEW.talks`. The blog map leaves room up to Lapland.

The map library ([jsvectormap](https://github.com/themustafaomar/jsvectormap) 1.5.3) is stored in `assets/js/jsvectormap/` and served from this site. Keep it that way: loading it from a CDN would send every visitor's IP address to that service, and the privacy policy (`_pages/terms.md`) says the site uses no external services.
