# Updating papers and talks

The publications list on `/research/` and the talks list on `/talks/` are generated from two data files. Adding a paper or a talk means adding an entry to one of them. The pages group entries by year, sort them, format author lists and dates, and highlight your name without any further edits.

| To add… | Edit |
|---|---|
| A paper, preprint or poster | `_data/publications.yml` |
| A talk, or another time you gave a talk | `_data/talks.yml` |

You only touch other files in two cases:

- **A venue that needs a new badge colour.** Add one line to `_sass/custom.scss` (see [Badges](#badges)).
- **A PDF you host yourself.** Put preprints in `assets/Preprints/` and posters in `assets/`, then link them as `/assets/Preprints/File.pdf` or `/assets/File.pdf`.

`_pages/research.md`, `_pages/talks.md` and the files in `_includes/` never need to change for a new entry.

---

## Adding a paper

Open `_data/publications.yml` and add an entry under `papers:`. Copy an existing one and edit it:

```yaml
papers:
  - title: "Your Paper Title"
    authors: [Mugdha Khedkar, Michael Schlichtig, Eric Bodden]
    venue: "Proceedings of the IEEE/ACM 48th International Conference on Software Engineering"
    year: 2027
    kind: Conference
    abbr: "ICSE'27"
    badge: pub-icse
    doi: 10.1145/1234567.1234568
    preprint: https://arxiv.org/abs/2701.00000
    artifacts: https://zenodo.org/records/0000000
```

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Shown in bold. |
| `authors` | yes | A list in square brackets. `Mugdha Khedkar` is highlighted wherever it appears. Commas and "and" are added for you. |
| `venue` | yes | Shown in grey italics. Include page numbers here if you want them. |
| `year` | yes | Decides which year group the paper appears in. |
| `kind` | no | Small grey label next to the badge: `Journal`, `Conference`, `Workshop`, `Doctoral Symposium`, … |
| `abbr` | yes | Text on the coloured badge. |
| `badge` | yes | Badge colour. See [Badges](#badges). |
| `doi` | no | Just the DOI, without `https://doi.org/`. Adds a **DOI** button and a **Copy citation** button. |
| `preprint` | no | Full URL, or `/assets/Preprints/File.pdf` for a PDF you host. Adds a **Preprint** button. |
| `artifacts` | no | Full URL. Adds an **Artifacts** button. |

**Order:** year groups are sorted newest first. Within a year, papers appear in the order they are written in the file, so put the one you want on top first.

### Preprints and posters

These go under `preprints:` and `posters:` in the same file. They use `links` instead of `doi`/`preprint`/`artifacts`, so you can name each button:

```yaml
preprints:
  - title: "Your Preprint Title"
    authors: [Mugdha Khedkar, Eric Bodden]
    venue: "arXiv:2701.00000 [cs.SE]"
    year: 2027
    kind: Preprint
    abbr: arXiv
    badge: arxiv
    links:
      - label: arXiv
        url: https://arxiv.org/abs/2701.00000

posters:
  - title: "Your Poster Title"
    venue: "Name of the event (EVENT 2027)"
    year: 2027
    kind: Poster
    abbr: "EVENT'27"
    badge: workshop
    links:
      - label: Poster PDF
        url: /assets/MyPoster2027.pdf
      - label: Event
        url: https://example.org/event
```

Preprints and posters are listed in file order and are not grouped by year.

**When a preprint gets published:** move its entry from `preprints:` to `papers:`. Then replace `links` with `doi`/`preprint`/`artifacts`, and update `venue`, `abbr` and `badge`.

---

## Adding a talk

Open `_data/talks.yml` and add an entry anywhere in the file:

```yaml
- title: "Your Talk Title"
  abbr: "Invited Talk"
  badge: invited-talk
  stops:
    - venue: "Security Group, University of Somewhere"
      flag: 🇳🇱
      date: "2026-11"
```

A talk at a conference, with the optional fields:

```yaml
- title: "Your Paper Title"
  abbr: "ICSE'27"
  badge: pub-icse
  kind: Conference talk
  award: "Best Presentation Award"
  stops:
    - venue: "48th International Conference on Software Engineering"
      url: https://conf.researchr.org/home/icse-2027
      co_label: FSE 2027
      co_url: https://conf.researchr.org/home/fse-2027
      flag: 🇨🇦
      date: "2027-04"
```

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Shown in bold. |
| `abbr` | yes | Text on the coloured badge. |
| `badge` | yes | Badge colour. See [Badges](#badges). |
| `kind` | no | Small grey label next to the badge, e.g. `Conference talk`, `Workshop talk`. |
| `award` | no | Shown as a red label with 🏆 under the talk. |
| `stops` | yes | One item per time you gave the talk. |
| `stops` → `venue` | yes | Where the talk was given. |
| `stops` → `flag` | yes | Country flag emoji. |
| `stops` → `date` | yes | `"YYYY-MM"`, **in quotes**. Shown as "Nov 2026". |
| `stops` → `url` | no | Turns the venue into a link. |
| `stops` → `co_label`, `co_url` | no | Adds "· co-located with …" after the venue. `co_url` makes it a link. |

**Order:** you don't need to think about it. Each talk goes under the year of its most recent date, and talks are sorted newest first. Talks from the same month keep their order in the file.

### Giving an existing talk again

Find the talk and add another item under its `stops`:

```yaml
- title: "Static Analysis for Android GDPR Compliance"
  abbr: "Invited Talk"
  badge: invited-talk
  stops:
    - venue: "New Place, New University"   # new
      flag: 🇫🇷
      date: "2026-12"
    - venue: "Cybersecurity Group, King's College London"
      flag: 🇬🇧
      date: "2025-12"
```

The talk moves to the year of its newest date. To show a repeat in a later year as a separate entry instead (like the 2026 Max Planck talk), add a new entry with the same title.

---

## Badges

Badge colours are defined at the top of `_sass/custom.scss`:

| `badge` | Colour | Used for |
|---|---|---|
| `pub-icse` | red | ICSE, SANER |
| `pub-mobilesoft` | green | MOBILESoft |
| `pub-asew` | blue | ASE workshops (A-Mobile) |
| `pub-asejournal` | yellow ochre | ASE Journal |
| `workshop` | magenta | workshops, posters |
| `arxiv` | grey | arXiv preprints |
| `phd-defense` | purple | PhD defence |
| `invited-talk` | teal | invited talks |
| `industry-talk` | orange | industry talks |

To add a new one, add a line next to the others and use its name as `badge`:

```scss
.pub-fse { background-color: #7c3aed; }  /* violet */
```

Badges use white text and must also show up on the dark-mode background (`#121212`). Mid-tone colours like the existing ones work. Very dark colours (navy, dark slate, dark teal) disappear in dark mode, and very light ones make the white text hard to read.

---

## Checking your change

From the `docs/` folder:

```bash
bundle exec jekyll serve
```

Then open http://localhost:4000/research/ or http://localhost:4000/talks/. The server rebuilds on its own when you save a file, so just refresh the page.

If the build fails, the terminal prints the error. The usual causes are:

- **Indentation.** Use spaces, never tabs, and line each field up with the entries around it.
- **Missing quotes.** Quote any text that contains `:` or `'`, e.g. `"SANER'26"` or `"Title: Subtitle"`.
- **Unquoted talk dates.** Write `date: "2026-11"`, not `date: 2026-11`.
