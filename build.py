"""Assemble the Witan site: wraps each page body in the shared header + footer.

Edit content in _src/*.html, then run:  python3 build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

PAGES = [
    # file, nav label, <title>
    ("index.html", "Home", "The Strategy Witan · 2027"),
    ("about.html", "About", "About · The Strategy Witan"),
    ("programme.html", "Programme", "Programme · The Strategy Witan"),
    ("blog.html", "Blog", "Blog · The Strategy Witan"),
    ("contact.html", "Contact", "Contact · The Strategy Witan"),
]


# Blog posts ("Notes from the Witan"). Body in _src/notes/<slug>.html,
# written to notes-<slug>.html. Newest first. Drafts show a banner.
POSTS = [
    # slug, title, date, tag, image, image credit, summary, draft
    ("strategy-should-no-longer-exist",
     "The motion passed: should strategy exist as a field?",
     "September 2026", "Oxford 2026 &middot; Debate",
     "assets/notes/debate.jpg",
     'Sa&iuml;d Business School, Oxford. Photo: pam fray, <a href="https://commons.wikimedia.org/wiki/File:The_Said_Business_School,_Oxford_-_geograph.org.uk_-_3939449.jpg">CC BY-SA 2.0</a>.',
     "A room of strategy scholars voted on whether their own field should be abolished. Here is how the argument &mdash; and the vote &mdash; went.",
     True),
    ("when-ai-meets-the-physical-world",
     "When AI meets the physical world",
     "September 2026", "Oxford 2026 &middot; Tech &amp; AI &middot; Tom Kwon",
     "assets/notes/physical-ai.jpg",
     'A self-driving car with roof-mounted LiDAR and cameras, San Francisco. Photo: Dllu, <a href="https://commons.wikimedia.org/wiki/File:Waymo_Jaguar_I-Pace_in_San_Francisco_2023_dllu.jpg">CC BY 4.0</a>.',
     "Robots, autonomous vehicles and drones make AI visible &mdash; and make one firm&rsquo;s mistakes everyone&rsquo;s strategy problem.",
     True),
    ("calibration-and-augmentation",
     "Very good at calibration, shy of augmentation",
     "September 2026", "Oxford 2026 &middot; Opening panel",
     "assets/notes/augmentation.jpg",
     'Engine houses at Botallack, Cornwall. Photo: Nilfanion, <a href="https://commons.wikimedia.org/wiki/File:Botallack_Crowns_engine_houses.jpg">CC BY-SA 3.0</a>.',
     "Are we perfecting a model of a world that has already moved on? A provocation from the opening panel.",
     True),
    ("slow-may-be-faster",
     "Slow may be faster: judgment in the age of AI",
     "September 2026", "Oxford 2026 &middot; Behavioural strategy",
     "assets/notes/slow.jpg",
     'Photo: Sebalston, <a href="https://commons.wikimedia.org/wiki/File:Pigeon_in_London.jpg">CC0</a>.',
     "More tools do not make better strategy. Two levers from the Carnegie tradition for learning when AI makes everything look plausible.",
     True),
    ("deference-may-be-dead",
     "Deference may be dead: strategy in institutional chaos",
     "September 2026", "Oxford 2026 &middot; Institutional theory",
     "assets/notes/chaos.jpg",
     'Howrah Bridge, Kolkata. Photo: Dey.sandip, <a href="https://commons.wikimedia.org/wiki/File:Howrah_Bridge,_Foggy.jpg">CC BY-SA 3.0</a>.',
     "When the yardsticks of legitimacy themselves are contested, what does strategy look like &mdash; and where are the openings?",
     True),
]


def note_card(p):
    slug, title, date, tag, img, _credit, summary, _draft = p
    return (f'<a class="ix-note" href="notes-{slug}.html">'
            f'<div class="ix-note-img"><img src="{img}" alt="" loading="lazy"></div>'
            f'<div class="ix-note-body"><span class="ix-note-tag">{tag}</span>'
            f'<h3>{title}</h3><p>{summary}</p>'
            f'<span class="ix-note-more">Read</span></div></a>')


def notes_carousel():
    cards = "\n".join(f"      {note_card(p)}" for p in POSTS)
    return f"""<div class="ix-carousel" data-carousel>
    <div class="ix-carousel-track">
{cards}
    </div>
    <div class="ix-carousel-nav">
      <button type="button" data-dir="-1" aria-label="Previous">&larr;</button>
      <button type="button" data-dir="1" aria-label="Next">&rarr;</button>
    </div>
  </div>"""


def notes_grid():
    return '<div class="ix-notes-grid">\n' + "\n".join(f"  {note_card(p)}" for p in POSTS) + "\n</div>"


CAROUSEL_SCRIPT = """
<script>
document.querySelectorAll('[data-carousel]').forEach(function (c) {
  var track = c.querySelector('.ix-carousel-track');
  c.querySelectorAll('[data-dir]').forEach(function (b) {
    b.addEventListener('click', function () {
      var card = track.querySelector('.ix-note');
      var step = card ? card.getBoundingClientRect().width + 24 : 320;
      track.scrollBy({ left: step * Number(b.dataset.dir), behavior: 'smooth' });
    });
  });
});
</script>"""


def post_page(p):
    slug, title, date, tag, img, credit, summary, draft = p
    body = (ROOT / "_src" / "notes" / f"{slug}.html").read_text().rstrip()
    banner = ('<p class="ix-draft">Draft for review &mdash; summarised from session notes; '
              'not yet checked with the speakers.</p>') if draft else ""
    return f"""<div class="page-header ix-post-header">
  <div class="shell">
    <p class="eyebrow">{tag}</p>
    <h1>{title}</h1>
    <p class="lede">{date}</p>
  </div>
</div>

<div class="shell page-body">
<article class="page ix-post">
  {banner}
  <figure class="figure ix-post-figure">
    <img src="{img}" alt="">
    <figcaption>{credit}</figcaption>
  </figure>
{body}
  <p class="ix-back"><a href="blog.html">&larr; All notes from the Witan</a></p>
</article>
</div>"""


# Full programmes (PDF) on Past editions. Keep False until Anil and Tom agree to
# publish them; then put the PDFs in assets/programmes/ and flip this to True.
PUBLISH_PROGRAMMES = False

PROGRAMME_FILES = {
    "2026": "assets/programmes/witan-2026-oxford-programme.pdf",
    "2019": "assets/programmes/london50-2019-programme.pdf",
}


def download(year):
    if PUBLISH_PROGRAMMES:
        return (f'<p class="download"><a href="{PROGRAMME_FILES[year]}" download>'
                f'Download the full programme (PDF)</a></p>')
    return ('<p class="download pending">Full programme with speakers and papers '
            '&mdash; PDF to be posted</p>')


def slug(text):
    text = re.sub(r"&[a-z]+;", "", text)
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def add_toc(body):
    """Give each <h2> an id and return (body, toc_html). Pages with fewer than
    two headings get no table of contents. An h2 can set data-toc="..." to use
    a shorter label in the sidebar."""
    entries = []

    def tag(m):
        attrs, label = m.group(1), m.group(2)
        short = re.search(r'data-toc="([^"]*)"', attrs)
        text = short.group(1) if short else label
        anchor = slug(text)
        entries.append((anchor, text))
        return f'<h2 id="{anchor}"{attrs}>{label}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", tag, body)
    if len(entries) < 2:
        return body, ""
    links = "\n".join(f'      <li><a href="#{a}">{t}</a></li>' for a, t in entries)
    toc = f'<aside class="toc">\n    <p class="toc-label">On this page</p>\n    <ul>\n{links}\n    </ul>\n  </aside>\n'
    return body, toc


TOC_SCRIPT = """
<script>
(function () {
  var links = document.querySelectorAll('.toc a');
  if (!links.length || !('IntersectionObserver' in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        links.forEach(function (a) { a.classList.remove('active'); });
        byId[e.target.id].classList.add('active');
      }
    });
  }, { rootMargin: '-15% 0px -70% 0px' });
  Object.keys(byId).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) obs.observe(el);
  });
})();
</script>"""


def nav(active):
    lines = []
    for href, label, _ in PAGES:
        cls = ' class="active"' if label == active else ''
        lines.append(f'      <a href="{href}"{cls}>{label}</a>')
    return "\n".join(lines)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="The Strategy Witan is an annual, invitation-only gathering of strategy scholars from across the UK. UCL School of Management hosts on 9 September 2027.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,25..100;1,9..144,300..700,25..100&family=Inter:wght@400;500;600&family=Oswald:wght@400;500;600&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="industry.css">
</head>
<body{body_class}>

<header class="site-header">
  <div class="shell-wide header-inner">
    <a class="ix-brand" href="index.html"><span>The Strategy</span><span>Witan</span></a>
    <nav>
{nav}
    </nav>
    <a class="ix-pill" href="contact.html">Get in touch</a>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <a class="ix-brand ix-brand-footer" href="index.html"><span>The Strategy</span><span>Witan</span></a>
      <p>Hosted by UCL School of Management in 2027. Bayes Business School in 2028.</p>
    </div>
    <p><a href="contact.html">Contact</a> &nbsp;·&nbsp; <a href="about.html">About</a></p>
  </div>
</footer>
{script}
</body>
</html>
"""

for fname, label, title in PAGES:
    body = (ROOT / "_src" / fname).read_text().rstrip()
    body = re.sub(r"\{\{download:(\d{4})\}\}", lambda m: download(m.group(1)), body)
    body = body.replace("{{notes:carousel}}", notes_carousel()).replace("{{notes:grid}}", notes_grid())
    toc = ""
    if fname != "index.html":
        body, toc = add_toc(body)
    if toc:
        body = body.replace('<div class="shell page-body">\n', '<div class="shell page-body">\n  ' + toc, 1)
    html = TEMPLATE.format(title=title, nav=nav(label), body=body,
                           body_class=' class="has-toc"' if toc else "",
                           script=(TOC_SCRIPT if toc else "") + (CAROUSEL_SCRIPT if "data-carousel" in body else ""))
    (ROOT / fname).write_text(html)
    print("built", fname)

for p in POSTS:
    html = TEMPLATE.format(title=f"{p[1]} · The Strategy Witan", nav=nav("Blog"),
                           body=post_page(p), body_class="", script="")
    (ROOT / f"notes-{p[0]}.html").write_text(html)
    print("built", f"notes-{p[0]}.html")
