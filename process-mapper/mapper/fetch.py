"""Fetch the sources listed in a service's sources.yaml and normalise them to plain text.

Each source becomes corpus/<service>/<source_id>.txt. Every text carries bracketed locator
markers ("[§ 7 Heading]", "[p. 3]", "[H2: How to apply]") so the extractor can cite positions
that a human can find again.

Usage:
  python -m mapper.fetch services/fi-kela-general-housing-allowance
"""

import hashlib
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import httpx
import yaml
from lxml import html as lxml_html
from pypdf import PdfReader

from .schema import Source

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (process-mapper prototype; research use)"}


# --------------------------------------------------------------------------------------
# Parsers: bytes -> text with locator markers
# --------------------------------------------------------------------------------------

def _clean(s: str) -> str:
    return re.sub(r"[ \t ]+", " ", s).strip()


def parse_akn(raw: bytes) -> str:
    """Akoma Ntoso act (Finlex open data) -> text, one '[§ N heading]' marker per section."""
    root = ET.fromstring(raw)

    def local(tag: str) -> str:
        return tag.rsplit("}", 1)[-1]

    # The consolidated endpoint returns a bundle (AknXmlList) with one document per language/version.
    # Keep the Finnish one with the latest consolidation date.
    if local(root.tag) == "AknXmlList":
        docs = [d for d in root.iter() if local(d.tag) == "akomaNtoso"]
        def is_fin(d):
            return any("/fin@" in (e.get("value") or "") for e in d.iter() if local(e.tag) == "FRBRthis")
        def consolidated_on(d):
            return max((e.get("date") or "" for e in d.iter() if local(e.tag) == "FRBRdate" and e.get("name") == "dateConsolidated"), default="")
        fin = [d for d in docs if is_fin(d)] or docs
        root = max(fin, key=consolidated_on)

    out = []
    title = root.find(".//{*}docTitle")
    if title is not None:
        out.append(f"[TITLE] {_clean(''.join(title.itertext()))}")
    for chapter in root.iter():
        if local(chapter.tag) == "chapter":
            num = chapter.find("{*}num")
            heading = chapter.find("{*}heading")
            out.append(
                f"\n[LUKU {_clean(''.join(num.itertext())) if num is not None else ''} "
                f"{_clean(''.join(heading.itertext())) if heading is not None else ''}]"
            )
            for section in chapter.iter():
                if local(section.tag) != "section":
                    continue
                snum = section.find("{*}num")
                shead = section.find("{*}heading")
                marker = _clean("".join(snum.itertext())) if snum is not None else "§ ?"
                head = _clean("".join(shead.itertext())) if shead is not None else ""
                out.append(f"\n[{marker} {head}]")
                for sub in section:
                    if local(sub.tag) in ("num", "heading"):
                        continue
                    text = _clean(" ".join(t for t in sub.itertext()))
                    if text:
                        out.append(text)
    if len(out) < 5:  # no chapters: fall back to flat section scan
        for section in root.iter():
            if local(section.tag) == "section":
                snum = section.find("{*}num")
                marker = _clean("".join(snum.itertext())) if snum is not None else "§ ?"
                out.append(f"\n[{marker}]")
                out.append(_clean(" ".join(section.itertext())))
    return "\n".join(out)


def parse_html(raw: bytes) -> str:
    """Web page -> text; headings become '[H2: title]' markers, element ids become '[#id]'."""
    doc = lxml_html.fromstring(raw)
    for bad in doc.xpath("//script|//style|//nav|//footer|//header|//noscript|//svg|//form"):
        bad.drop_tree()
    main = doc.xpath("//main") or doc.xpath("//article") or [doc.body if doc.body is not None else doc]
    out = []
    for el in main[0].iter():
        if not isinstance(el.tag, str):
            continue
        tag = el.tag.lower()
        if tag in ("h1", "h2", "h3", "h4"):
            t = _clean(el.text_content())
            if t:
                anchor = el.get("id")
                out.append(f"\n[{tag.upper()}: {t}]" + (f" [#{anchor}]" if anchor else ""))
        elif tag in ("p", "li", "td", "th", "dt", "dd", "summary"):
            t = _clean(el.text_content())
            if t and (not out or t not in out[-1]):
                out.append(t)
    return "\n".join(out)


def parse_pdf(raw: bytes) -> str:
    reader = PdfReader(io.BytesIO(raw))
    out = []
    for i, page in enumerate(reader.pages, 1):
        out.append(f"\n[p. {i}]")
        out.append(_clean_lines(page.extract_text() or ""))
    return "\n".join(out)


def _clean_lines(s: str) -> str:
    return "\n".join(_clean(line) for line in s.splitlines() if _clean(line))


def parse_ptv(raw: bytes) -> str:
    """PTV service record (JSON) -> readable text with the fields that describe the service."""
    s = json.loads(raw)

    def lang(items, language="fi", key="value"):
        return [i.get(key) for i in items or [] if i.get("language") == language and i.get(key)]

    out = [f"[PTV service {s.get('id')}]"]
    for language in ("fi", "en"):
        names = lang(s.get("serviceNames"), language)
        if names:
            out.append(f"Name ({language}): {'; '.join(names)}")
    out.append(f"Type: {s.get('type')}  Funding: {s.get('fundingType')}  Charge: {s.get('serviceChargeType')}")
    out.append("Organisations: " + "; ".join(
        f"{o.get('organization', {}).get('name')} ({o.get('roleType')})" for o in s.get("organizations") or []))
    for d in s.get("serviceDescriptions") or []:
        if d.get("language") in ("fi", "en") and d.get("value"):
            out.append(f"\n[Description:{d.get('type')} ({d.get('language')})]\n{d['value']}")
    req = lang(s.get("requirements"), "fi") + lang(s.get("requirements"), "en")
    out.append("\n[Requirements]\n" + ("\n".join(req) if req else "(empty)"))
    out.append("\n[Legislation]\n" + (json.dumps(s.get("legislation"), ensure_ascii=False) if s.get("legislation") else "(empty)"))
    out.append("\n[Life events] " + "; ".join(
        n["value"] for le in s.get("lifeEvents") or [] for n in le.get("name", []) if n.get("language") == "en"))
    out.append("[Service classes] " + "; ".join(
        n["value"] for sc in s.get("serviceClasses") or [] for n in sc.get("name", []) if n.get("language") == "en"))
    out.append("[Target groups] " + "; ".join(
        n["value"] for tg in s.get("targetGroups") or [] for n in tg.get("name", []) if n.get("language") == "en"))
    channels = [c.get("serviceChannel", {}).get("name") for c in s.get("serviceChannels") or []]
    digital = [c for c in channels if c and not c.startswith("Kela ") and "palvelupiste" not in c.lower()]
    out.append(f"\n[Service channels] {len(channels)} channels in total; non-office channels: {'; '.join(sorted(set(digital)))}")
    out.append(f"Office / service point channels: {sum(1 for c in channels if c and c not in digital)}")
    return "\n".join(out)


PARSERS = {"akn_xml": parse_akn, "html": parse_html, "pdf": parse_pdf, "ptv_api": parse_ptv}


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------

def fetch_service(service_dir: Path) -> list[Source]:
    cfg = yaml.safe_load((service_dir / "sources.yaml").read_text())
    service_id = cfg["service_id"]
    corpus_dir = ROOT / "corpus" / service_id
    corpus_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = corpus_dir / "_raw"
    raw_dir.mkdir(exist_ok=True)

    sources: list[Source] = []
    with httpx.Client(headers=UA, follow_redirects=True, timeout=60) as client:
        for entry in cfg["sources"]:
            src = Source(**{k: v for k, v in entry.items() if k in Source.model_fields})
            raw_path = raw_dir / f"{src.id}.{ 'xml' if src.kind=='akn_xml' else 'json' if src.kind=='ptv_api' else 'pdf' if src.kind=='pdf' else 'html'}"
            if raw_path.exists():
                raw = raw_path.read_bytes()
                print(f"  {src.id}: cached raw ({len(raw)} B)")
            else:
                r = client.get(src.url)
                r.raise_for_status()
                raw = r.content
                raw_path.write_bytes(raw)
                print(f"  {src.id}: fetched {len(raw)} B")
            text = PARSERS[src.kind](raw)
            (corpus_dir / f"{src.id}.txt").write_text(text)
            src.fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            src.chars = len(text)
            src.sha256 = hashlib.sha256(raw).hexdigest()[:16]
            sources.append(src)
            print(f"      -> {src.chars} chars of text, layer={src.layer}")

    manifest = {"service_id": service_id, "sources": [s.model_dump() for s in sources]}
    (corpus_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"\nWrote {corpus_dir / 'manifest.json'}")
    return sources


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    fetch_service(Path(sys.argv[1]).resolve())
