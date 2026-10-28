"""Render a map into the guided landing page and a Mermaid flowchart.

  site/template.html  +  maps/<svc>/{map,report,facts}.json  +  corpus/<svc>/manifest.json
      -> site/<svc>.html   (self-contained: data embedded as JSON)
      -> maps/<svc>/map.mmd

Usage:
  python -m mapper.render services/fi-kela-general-housing-allowance
"""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def mermaid(pm: dict) -> str:
    shape = {
        "start_event": ("((", "))"), "end_event": ("(((", ")))"), "decision": ("{", "}"),
        "wait": ("[/", "/]"), "timer": ("[/", "/]"),
    }
    lines = ["flowchart LR"]
    actors = {a["id"]: a["name"] for a in pm["actors"]}
    by_actor: dict[str, list] = {}
    for n in pm["nodes"]:
        by_actor.setdefault(n["actor_id"], []).append(n)
    for actor_id, nodes in by_actor.items():
        lines.append(f'  subgraph {actor_id}["{actors.get(actor_id, actor_id)}"]')
        for n in nodes:
            o, c = shape.get(n["type"], ("[", "]"))
            label = n["name"].replace('"', "'")
            lines.append(f'    {n["id"]}{o}"{label}"{c}')
        lines.append("  end")
    for e in pm["edges"]:
        cond = f'|"{e["condition"].replace(chr(34), chr(39))}"|' if e.get("condition") else ""
        lines.append(f'  {e["source"]} -->{cond} {e["target"]}')
    for n in pm["nodes"]:
        if n["grounding"] == "inferred":
            lines.append(f"  style {n['id']} stroke-dasharray: 5 5")
    return "\n".join(lines)


LANDING_EXAMPLE_URL = "https://claude.ai/artifact/Ny89PLSUukS65dgaFZQqwr"
LANDING_URL = "https://claude.ai/artifact/1QtqzmiNniqopWiHWX3UhF"
DOCS = ROOT.parent / "docs"  # standalone pages for GitHub Pages (serve from main /docs)

SKELETON_HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                 '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n')


def write_standalone(fragment: str, name: str) -> Path:
    """The artifact host wraps fragments in its own skeleton; for GitHub Pages we add one ourselves
    and point the two pages at each other with relative links."""
    cut = fragment.index("</style>") + len("</style>")
    head, body = fragment[:cut], fragment[cut:]
    html = SKELETON_HEAD + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n"
    html = html.replace(LANDING_EXAMPLE_URL, "fi-kela-general-housing-allowance.html").replace(LANDING_URL, "index.html")
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").touch()
    out = DOCS / name
    out.write_text(html)
    print(f"Wrote {out} ({len(html)//1024} KB, standalone)")
    return out


def render_landing(service_dir: Path) -> Path:
    """The general landing page, with the service's map as its live illustration."""
    import statistics
    cfg = yaml.safe_load((service_dir / "sources.yaml").read_text())
    sid = cfg["service_id"]
    maps_dir = ROOT / "maps" / sid
    pm = json.loads((maps_dir / "map.json").read_text())
    report = json.loads((maps_dir / "report.json").read_text())
    manifest = json.loads((ROOT / "corpus" / sid / "manifest.json").read_text())
    nodes = [{k: n[k] for k in ("id", "name", "type", "actor_id", "visibility", "automation_class", "agent_mode", "confidence")} for n in pm["nodes"]]
    edges = [{"s": e["source"], "t": e["target"]} for e in pm["edges"]]
    by_vis = lambda v: [n["confidence"] for n in pm["nodes"] if n["visibility"] == v]
    step = next((n for n in pm["nodes"] if n["id"] == "T_CALC"), pm["nodes"][len(pm["nodes"]) // 3])
    ex_step = {k: step[k] for k in ("id", "name", "type", "actor_id", "visibility", "inputs", "data_source_ids", "rule_ids", "automation_class", "agent_mode", "agent_mode_reason", "grounding", "confidence", "validated")}
    ex_step["provenance"] = [{k: p[k] for k in ("source_id", "locator", "quote")} for p in step["provenance"][:1]]
    ex_step["provenance_count"] = len(step["provenance"])
    rule = next((r for r in pm["rules"] if r["id"] in step["rule_ids"] and r["kind"] == "calculation"), pm["rules"][0])
    ex_rule = {k: rule[k] for k in ("id", "name", "kind", "logic")}
    ex_rule["parameters"] = rule["parameters"][:4]
    ex_rule["provenance_count"] = len(rule["provenance"])
    data = {
        "nodes": nodes, "edges": edges, "actors": {a["id"]: a["name"] for a in pm["actors"]},
        "report": {**report, "sources_count": len(manifest["sources"]), "actors": len(pm["actors"]), "processes": sum(1 for n in pm["nodes"] if n["type"] == "start_event") - 1,
                   "provenance_pct": round(100 * report.get("facts_used_in_map", 0) / max(1, report["facts_verified"]))},
        "means": {"external": statistics.mean(by_vis("external")), "internal": statistics.mean(by_vis("internal"))},
        "example_step": ex_step, "example_rule": ex_rule, "example_url": LANDING_EXAMPLE_URL,
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = (ROOT / "site" / "landing_template.html").read_text().replace("/*__DATA__*/null", payload)
    out = ROOT / "site" / "index.html"
    out.write_text(html)
    print(f"Wrote {out} ({len(html)//1024} KB)")
    write_standalone(html, "index.html")
    return out


def render(service_dir: Path) -> Path:
    cfg = yaml.safe_load((service_dir / "sources.yaml").read_text())
    sid = cfg["service_id"]
    maps_dir = ROOT / "maps" / sid
    pm = json.loads((maps_dir / "map.json").read_text())
    report = json.loads((maps_dir / "report.json").read_text())
    facts = json.loads((maps_dir / "facts.json").read_text())
    rejected = json.loads((maps_dir / "facts_rejected.json").read_text())
    manifest = json.loads((ROOT / "corpus" / sid / "manifest.json").read_text())

    # a handful of verified facts per source for the "how we do it" section
    examples = []
    rejected_ids = {f["id"] for f in rejected}
    for sheet in facts["sheets"]:
        picked = [f for f in sheet["facts"] if f["id"] not in rejected_ids and f["kind"] in ("step", "calculation", "deadline", "data_source")][:3]
        examples.extend(picked)

    data = {
        "service_cfg": {k: cfg[k] for k in ("service_id", "service_name", "country", "authority")},
        "manifest": manifest,
        "map": pm,
        "report": report,
        "example_facts": examples,
        "rejected_examples": rejected[:5],
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = (ROOT / "site" / "template.html").read_text()
    html = template.replace("/*__DATA__*/null", payload)
    out = ROOT / "site" / f"{sid}.html"
    out.write_text(html)
    write_standalone(html, f"{sid}.html")
    (maps_dir / "map.mmd").write_text(mermaid(pm))
    print(f"Wrote {out} ({len(html)//1024} KB) and {maps_dir / 'map.mmd'}")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    render(Path(sys.argv[1]).resolve())
    render_landing(Path(sys.argv[1]).resolve())
