# The Strategy Witan — working notes for Claude

The Strategy Witan is an annual, invitation-only conference for the UK strategy community. UCL School of Management hosts in September 2027; Bayes Business School hosts in 2028.

Live at https://witan.tomkwon.com (subdomain of Tom's personal site while we get set up; may migrate to a dedicated domain later — see "Not decided yet" below).
Served by GitHub Pages from `main` of `tomhykwon/witan`.

Tom talks in Korean — reply in Korean.

## How the site is built

Same pattern as `tomkwon.com`:

- `_src/*.html` — **edit content here** (page bodies only).
- `build.py` — wraps each page body in the shared header, nav and footer. Nav labels and `<title>`s live in the `PAGES` list here.
- Run `python3 build.py` → writes root HTML files (`index.html`, `about.html`, etc.). **Never edit the root HTML files by hand** — they are overwritten on every build.
- `style.css` — all styling. Colour tokens at the top (`--bg` warm paper, `--accent` UCL deep purple `#3b2159`, `--rule` hairline warm grey).
- `_config.yml` excludes build files from Jekyll; `_src/` is ignored by Jekyll because of the underscore prefix.
- `CNAME` = `witan.tomkwon.com`.

## Workflow

1. Preview locally: `python3 -m http.server 4000 --directory ~/code/witan` (in the Claude app, use `preview_start` on a launch.json entry).
2. Edit `_src/` or `style.css` / `build.py`, run `python3 build.py`, check the preview.
3. Commit and `git push` — GitHub Pages redeploys in ~1–2 min.
4. DNS: `witan` CNAME → `tomhykwon.github.io` (Squarespace Domains, in Tom's account). Tom needs to add this record manually before the subdomain resolves.

## Design principles

- Clean, professional, academic. Nothing that "튀어" or looks AI-generated: no cards, no gradients, no big stat blocks, no loud badges.
- Emphasis is subtle: small uppercase purple labels for section headings, thin hairline rules, single-column ≤ 720px.
- Serif body (Source Serif 4), sans for nav and small labels (Source Sans 3).
- Borrows the philosophy of `tomkwon.com` but is intentionally not identical — the Witan is not Tom's personal site. No site-wide sidebar nav. Subpages with 2+ `<h2>` sections get an auto-generated sticky "On this page" list on the left (built by `build.py` from the h2s; `data-toc="..."` sets a shorter label; hidden under 1040px). Home and Blog have none.

## Content rules

- **Don't invent facts.** Source from the planning doc (`/Users/tom/Library/CloudStorage/OneDrive-UniversityCollegeLondon/# Conferences/2027 WITAN/`) or ask Tom.
- Currently uncertain — do not commit these as fact on the site until confirmed:
  - ~~Exact date~~ — confirmed by Tom 2026-09-29: Thursday 9 September 2027.
  - RSVP link (invitations expected ~January 2027)
  - Programme structure
  - UCL colleague names as session leads (Rohan / Jen / Chris / Sukanya — sound-out only, not yet confirmed)
- 2019 London 50 organiser: Freek Vermeulen (confirmed from Oxford 2026 welcome doc). Held Thursday 30 May 2019 (2019 agenda docx).
- Oxford 2026 was Thursday 10 September 2026 (Day Programme docx).
- Hosts: always list **Anil Doshi first** (senior), then Tom Kwon. Anil's email: anil.doshi@ucl.ac.uk (confirmed 2026-09-29).
- UCL SoM floors at One Canada Square: Levels 38, 48, 49, 50 in use (48 newly opened); Levels 46 and 47 due to open.
- Home page shows logos of **all** participating schools (from 2019/2026 attendee lists), **alphabetical**, greyscale (colour on hover), in `assets/logos/`. Tom chose logos over text (2026-09-29). Never drop a school or rank them.
- Organisers (confirmed by Tom 2026-09-29): Oxford 2026 = Michelle Rogan, Richard Whittington, Eric Zhao. Bayes 2028 = Santi Furnari, Gianvito Lanzolla, Elena Novelli.
- Past editions shows detailed programmes **without speaker names**. Full programme PDFs are gated by `PUBLISH_PROGRAMMES` in `build.py` (False until Anil & Tom agree); PDFs go in `assets/programmes/`. Attendee/invite lists are never published.

## Pages

- `index.html` — Home (dark editorial hero, what is a Witan, rotation)
- `about.html` — extended history, etymology (with medieval witan-council image), format, the 2027 host (with UCL Portico image), rotation
- `past.html` — Oxford 2026 (later: 2027 archived after the event, then 2028 etc.)
- `blog.html` — "Notes from the Witan" — placeholder for now; first posts late 2026
- `contact.html` — organisers, venue (with Canary Wharf image), attending, hosting-a-future-Witan

## Assets

Images live in `assets/`. Currently:
- `witan-council.jpg` — medieval manuscript of an Anglo-Saxon witan council. Used in About > "The name".
- `ucl-portico.jpg` — UCL Portico with UCL200 bicentenary branding. Used in About > "The 2027 host".
- `canary-wharf.webp` — One Canada Square (UCL SoM's building). Used in Contact > "Venue".

Figure/caption styling lives in `style.css` under "Figures". Images render full-width of the content column with a thin border and a small sans caption below.

## Handoff (2028 → Bayes)

The site is designed to be inherited. What Bayes will need:
- This repo (Tom can transfer ownership or grant write access)
- The `witan.tomkwon.com` subdomain migrates to whatever Bayes prefers by changing `CNAME` file + DNS
- The `build.py` + `_src/` pattern is intentionally simple — a colleague with basic Python/Git familiarity can maintain it
- **The blog is the mechanism that survives rotating hosts.** Bayes is asked to continue publishing.

## Not decided yet

- Whether we buy a dedicated domain (`strategywitan.org` etc.) or stay on the subdomain — decision deferred, low cost either way.
- Whether to add a formal Programme page (currently folded into Home).
- Whether the blog gets its own posts directory (`_posts/` with per-post files) or stays as a manually-updated list.
- Colour: UCL deep purple as accent is the current default (UCL is 2027 host). Future hosts may want to change this — the accent lives in `style.css` as `--accent`.
