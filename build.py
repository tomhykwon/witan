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
    ("past.html", "Past editions", "Past editions · The Strategy Witan"),
    ("blog.html", "Blog", "Blog · The Strategy Witan"),
    ("contact.html", "Contact", "Contact · The Strategy Witan"),
]


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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,25..100;1,9..144,300..700,25..100&family=Inter:wght@400;500;600&family=Inter+Tight:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
    toc = ""
    if fname != "index.html":
        body, toc = add_toc(body)
    if toc:
        body = body.replace('<div class="shell page-body">\n', '<div class="shell page-body">\n  ' + toc, 1)
    html = TEMPLATE.format(title=title, nav=nav(label), body=body,
                           body_class=' class="has-toc"' if toc else "",
                           script=TOC_SCRIPT if toc else "")
    (ROOT / fname).write_text(html)
    print("built", fname)
