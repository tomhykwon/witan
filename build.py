"""Assemble the Witan site: wraps each page body in the shared header + footer.

Edit content in _src/*.html, then run:  python3 build.py
"""
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,25..100;1,9..144,300..700,25..100&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>

<header class="site-header">
  <div class="shell-wide header-inner">
    <a class="site-name" href="index.html">The Strategy <span class="site-name-mark">Witan</span></a>
    <nav>
{nav}
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <span class="footer-mark">The Strategy Witan</span>
      <p>Hosted by UCL School of Management in 2027. Bayes Business School in 2028.</p>
    </div>
    <p><a href="contact.html">Contact</a> &nbsp;·&nbsp; <a href="about.html">About</a></p>
  </div>
</footer>

</body>
</html>
"""

for fname, label, title in PAGES:
    body = (ROOT / "_src" / fname).read_text().rstrip()
    html = TEMPLATE.format(title=title, nav=nav(label), body=body)
    (ROOT / fname).write_text(html)
    print("built", fname)
