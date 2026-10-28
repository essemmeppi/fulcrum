"""Bundle the two pages in docs/ into one self-contained HTML file for sharing.

docs/index.html (landing) and docs/fi-kela-general-housing-allowance.html (demo) stay the source of
truth. This script reads them and writes share/the-agentic-state.html: one file, the shared header on
top, the landing as the first view and the demo as the second. The Home / Demo links switch views
(#home / #demo in the URL); everything else is copied as is. The favicon is inlined so the file works
alone, anywhere. Fonts still come from Google Fonts, with system fallbacks when offline.

Usage:
  python -m mapper.bundle
"""

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT.parent / "docs"
OUT = ROOT.parent / "share" / "the-agentic-state.html"

LANDING = DOCS / "index.html"
DEMO = DOCS / "fi-kela-general-housing-allowance.html"

FONTS = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@1,6..72,300"
         "&family=Inter:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap")

# Selectors styled once for the whole file (tokens, body, shared header); everything else is scoped per view.
SHARED_PREFIXES = (":root", "html", "body", "*", "header.top")


# ---------- CSS ----------

def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def rules(css: str):
    """Yield (prelude, body) for each top-level block, nesting-aware."""
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        depth, k = 0, j
        while k < n:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        yield prelude, css[j + 1:k]
        i = k + 1


def is_shared(selector: str) -> bool:
    return selector.startswith(SHARED_PREFIXES)


def scope_css(css: str, scope: str) -> str:
    """Prefix every selector with `scope`, drop shared selectors, keep @keyframes as they are."""
    out = []
    for prelude, body in rules(strip_comments(css)):
        if prelude.startswith(("@media", "@supports")):
            inner = scope_css(body, scope)
            if inner.strip():
                out.append(f"{prelude} {{\n{inner}\n}}")
        elif prelude.startswith("@"):
            out.append(f"{prelude} {{{body}}}")
        else:
            kept = [f"{scope} {s.strip()}" for s in prelude.split(",") if not is_shared(s.strip())]
            if kept:
                out.append(", ".join(kept) + " {" + body + "}")
    return "\n".join(out)


def shared_css(css: str, keep) -> str:
    """Keep only the rules whose selectors pass `keep`, descending into @media."""
    out = []
    for prelude, body in rules(strip_comments(css)):
        if prelude.startswith(("@media", "@supports")):
            inner = shared_css(body, keep)
            if inner.strip():
                out.append(f"{prelude} {{\n{inner}\n}}")
        elif prelude.startswith("@"):
            continue
        else:
            kept = [s.strip() for s in prelude.split(",") if keep(s.strip())]
            if kept:
                out.append(", ".join(kept) + " {" + body + "}")
    return "\n".join(out)


# ---------- HTML pieces ----------

def main_style(html: str) -> str:
    blocks = re.findall(r"<style>(.*?)</style>", html, flags=re.S)
    return max(blocks, key=len)  # the first <style> is the one-line reset


def body_inner(html: str) -> str:
    m = re.search(r"<body>(.*)</body>", html, flags=re.S)
    inner = m.group(1)
    inner = re.sub(r"<header class=\"top\">.*?</header>", "", inner, count=1, flags=re.S)
    inner = re.sub(r"<script>.*?</script>", "", inner, flags=re.S)
    return inner.strip("\n")


def script_inner(html: str) -> str:
    m = re.search(r"<body>.*<script>(.*?)</script>", html, flags=re.S)
    return m.group(1)


def deferred(script: str, name: str) -> str:
    """Turn the demo's self-running `(function () { ... })();` into `window.<name> = function () { ... };`
    so the map is drawn the first time the demo view is shown and can measure its box."""
    head, sep, rest = script.partition("(function () {")
    if not sep:
        sys.exit("demo script: opening `(function () {` not found")
    body, sep2, tail = rest.rpartition("})();")
    if not sep2:
        sys.exit("demo script: closing `})();` not found")
    return f"{head}window.{name} = function () {{{body}}};{tail}"


def build() -> Path:
    landing = LANDING.read_text(encoding="utf-8")
    demo = DEMO.read_text(encoding="utf-8")

    l_css, d_css = main_style(landing), main_style(demo)
    d_css = re.sub(r"\bmarch\b", "march-demo", d_css)  # both pages animate dashes; keep the periods apart

    css = "\n".join([
        "/* shared: tokens and body from the landing page, extra tokens from the demo */",
        shared_css(l_css, lambda s: s.startswith((":root", "*", "body", "html"))),
        shared_css(d_css, lambda s: s.startswith(":root")),
        "/* shared header */",
        shared_css(l_css, lambda s: s.startswith("header.top")),
        "header.top .mark { color: var(--fg); }",
        ".view[hidden] { display: none; }",
        "/* landing */",
        scope_css(l_css, "#view-home"),
        "/* demo */",
        scope_css(d_css, "#view-demo"),
    ])

    l_body = body_inner(landing)
    d_body = body_inner(demo).replace('id="legend"', 'id="legend-demo"')  # the landing owns #legend

    l_js = script_inner(landing)
    d_js = deferred(script_inner(demo), "initDemo")

    icon = base64.b64encode((DOCS / "favicon" / "favicon-32x32.png").read_bytes()).decode()

    router = """
(function () {
  // The view containers are not named after the hash on purpose: the browser must not scroll to them itself.
  const views = { home: document.getElementById('view-home'), demo: document.getElementById('view-demo') };
  const links = [...document.querySelectorAll('header.top nav a')];
  let current = null, demoReady = false;
  function show(v) {
    if (v === current) return;
    current = v;
    for (const k in views) views[k].hidden = k !== v;
    links.forEach(a => a.classList.toggle('current', a.getAttribute('href') === '#' + v));
    if (v === 'demo' && !demoReady) { demoReady = true; window.initDemo(); }
  }
  function route() {
    const h = decodeURIComponent(location.hash.slice(1));
    if (views[h]) { show(h); window.scrollTo({ top: 0, behavior: 'instant' }); return; }
    const el = h && document.getElementById(h);
    const owner = el && el.closest('.view');
    if (owner) { show(owner.dataset.view); el.scrollIntoView(); return; }
    show(current || 'home');
  }
  const ex = document.getElementById('example-link');
  if (ex) { ex.href = '#demo'; ex.removeAttribute('target'); ex.removeAttribute('rel'); }
  window.addEventListener('hashchange', route);
  route();
})();
"""

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<title>The Agentic State</title>
<link rel="icon" type="image/png" href="data:image/png;base64,{icon}">
<link rel="stylesheet" href="{FONTS}">
<style>
{css}
</style>
</head>
<body>

<header class="top">
  <a class="mark" href="https://agenticstate.org" target="_blank" rel="noopener">The Agentic State</a>
  <nav><a href="#home" class="current">Home</a><a href="#demo">Demo</a></nav>
</header>

<div id="view-home" class="view" data-view="home">
{l_body}
</div>

<div id="view-demo" class="view" data-view="demo" hidden>
{d_body}
</div>

<script>
{{
{l_js.strip()}
}}
</script>
<script>
{{
{d_js.strip()}
}}
</script>
<script>{router}</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    out = build()
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB)")
