"""Refresh the data embedded in the two hand-edited pages in docs/.

docs/index.html and docs/<service>.html are the source of truth and are edited by hand. This script only
replaces the `const DATA = ...;` line in each of them with fresh numbers from maps/<service>/ and
corpus/<service>/manifest.json, and writes maps/<service>/map.mmd. It never regenerates the pages.

Usage:
  python -m mapper.render services/fi-kela-general-housing-allowance
"""

import json
import re
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


DOCS = ROOT.parent / "docs"


def refresh_data(page: Path, data: dict) -> None:
    """Replace the embedded DATA constant in a page, leaving everything else untouched."""
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = page.read_text()
    new, n = re.subn(r"const DATA = .*?;\n", "const DATA = " + payload.replace("\\", "\\\\") + ";\n", html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"{page}: could not find the `const DATA = ...;` line")
    page.write_text(new)
    print(f"Refreshed data in {page} ({len(new)//1024} KB)")


TASK_TYPES = ("citizen_task", "caseworker_task", "system_task", "third_party_task")


def first_process(pm: dict) -> tuple[list[dict], list[dict]]:
    """The steps reachable from the service's first start event without crossing another start event."""
    starts = [n["id"] for n in pm["nodes"] if n["type"] == "start_event"]
    out: dict[str, list[str]] = {}
    for e in pm["edges"]:
        out.setdefault(e["source"], []).append(e["target"])
    seen, stack = {starts[0]}, [starts[0]]
    while stack:
        for v in out.get(stack.pop(), []):
            if v in starts[1:] or v in seen:
                continue
            seen.add(v)
            stack.append(v)
    nodes = [n for n in pm["nodes"] if n["id"] in seen]
    edges = [e for e in pm["edges"] if e["source"] in seen and e["target"] in seen]
    return nodes, edges


def contract(nodes: list[dict], edges: list[dict]) -> tuple[dict, list[dict]]:
    """Illustrative redesign. Rule 1: consecutive steps by the same actor doing the same kind of work
    merge. Rule 2: a decision merges into the preceding step when both are by the same actor and of
    the same kind (the check becomes part of the step). Rule 3: loops are drawn once (back-edges dropped).
    Returns (rep: original id -> representative id, contracted edges)."""
    N = {n["id"]: n for n in nodes}
    rep = {n["id"]: n["id"] for n in nodes}
    E = {(e["source"], e["target"]) for e in edges}

    def degrees():
        o, i = {}, {}
        for a, b in E:
            o.setdefault(a, set()).add(b)
            i.setdefault(b, set()).add(a)
        return o, i

    def merge(b, a):
        nonlocal E
        E = {(a if x == b else x, a if y == b else y) for (x, y) in E}
        E = {(x, y) for (x, y) in E if x != y}
        for k, v in rep.items():
            if v == b:
                rep[k] = a

    changed = True
    while changed:
        changed = False
        o, i = degrees()
        for a, b in sorted(E):
            A, B = N[a], N[b]
            same = A["actor_id"] == B["actor_id"] and A["automation_class"] == B["automation_class"]
            chain = A["type"] in TASK_TYPES and B["type"] in TASK_TYPES and len(o.get(a, ())) == 1 and len(i.get(b, ())) == 1
            check = A["type"] in TASK_TYPES and B["type"] == "decision" and len(i.get(b, ())) == 1
            if same and (chain or check):
                merge(b, a)
                changed = True
                break
    # rule 3: drop back-edges (longest-path ranks, DFS-based)
    start = next(n["id"] for n in nodes if n["type"] == "start_event")
    color, order, back = {}, [], set()
    o, _ = degrees()

    def dfs(u):
        color[u] = 1
        for v in sorted(o.get(u, ())):
            if color.get(v) == 1:
                back.add((u, v))
            elif v not in color:
                dfs(v)
        color[u] = 2
        order.append(u)

    dfs(rep[start])
    E = {(a, b) for (a, b) in E if (a, b) not in back}
    return rep, [{"s": a, "t": b} for a, b in sorted(E)]


def render_landing(service_dir: Path) -> None:
    """The general landing page, with one process of the service as its live illustration."""
    import statistics
    cfg = yaml.safe_load((service_dir / "sources.yaml").read_text())
    sid = cfg["service_id"]
    maps_dir = ROOT / "maps" / sid
    pm = json.loads((maps_dir / "map.json").read_text())
    report = json.loads((maps_dir / "report.json").read_text())
    manifest = json.loads((ROOT / "corpus" / sid / "manifest.json").read_text())
    p_nodes, p_edges = first_process(pm)
    rep, r_edges = contract(p_nodes, p_edges)
    nodes = [{k: n[k] for k in ("id", "name", "type", "actor_id", "visibility", "automation_class", "agent_mode", "confidence")} for n in p_nodes]
    edges = [{"s": e["source"], "t": e["target"]} for e in p_edges]
    process_name = next(n["name"] for n in p_nodes if n["type"] == "start_event")
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
        "process_name": process_name, "redesign": {"rep": rep, "edges": r_edges},
        "service_totals": {"nodes": len(pm["nodes"]), "edges": len(pm["edges"])},
        "report": {**report, "sources_count": len(manifest["sources"]), "actors": len(pm["actors"]), "processes": sum(1 for n in pm["nodes"] if n["type"] == "start_event") - 1,
                   "provenance_pct": round(100 * report.get("facts_used_in_map", 0) / max(1, report["facts_verified"]))},
        "means": {"external": statistics.mean(by_vis("external")), "internal": statistics.mean(by_vis("internal"))},
        "example_step": ex_step, "example_rule": ex_rule, "example_url": f"{sid}.html",
    }
    refresh_data(DOCS / "index.html", data)


def render(service_dir: Path) -> None:
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
    refresh_data(DOCS / f"{sid}.html", data)
    (maps_dir / "map.mmd").write_text(mermaid(pm))
    print(f"Wrote {maps_dir / 'map.mmd'}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    render(Path(sys.argv[1]).resolve())
    render_landing(Path(sys.argv[1]).resolve())
