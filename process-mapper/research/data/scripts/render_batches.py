"""Render a variant map's nodes into verification batch files (same format as e2 batches)."""
import json, sys
from pathlib import Path
path, tag, nb = sys.argv[1], sys.argv[2], int(sys.argv[3])
m = json.load(open(path))
actors = {a["id"]: a.get("name", a["id"]) for a in m.get("actors", [])}
nodes = {n["id"]: n for n in m["nodes"]}
preds, succs = {}, {}
for e in m["edges"]:
    succs.setdefault(e["source"], []).append((e["target"], e.get("condition") or ""))
    preds.setdefault(e["target"], []).append((e["source"], e.get("condition") or ""))
def render(n):
    out = [f"NODE {n['id']}", f"  name: {n['name']}", f"  description: {n.get('description','')}",
           f"  type: {n.get('type')}; actor: {actors.get(n.get('actor_id'), n.get('actor_id'))} ({n.get('actor_id')}); visibility: {n.get('visibility')}",
           f"  automation_class: {n.get('automation_class')}; agent_mode: {n.get('agent_mode')}; confidence (model's own): {n.get('confidence')}"]
    out.append("  predecessors: " + ("; ".join(f"{p} ({nodes[p]['name']})" + (f" [if: {c}]" if c else "") for p, c in preds.get(n["id"], []) if p in nodes) or "none"))
    out.append("  successors: " + ("; ".join(f"{s} ({nodes[s]['name']})" + (f" [if: {c}]" if c else "") for s, c in succs.get(n["id"], []) if s in nodes) or "none"))
    ev = n.get("evidence") or []
    out.append(f"  public-source evidence: {len(ev)} quote(s) from {sorted(set(e.get('source','') for e in ev))}")
    if n.get("inferred_reason"): out.append(f"  inferred_reason: {n['inferred_reason']}")
    return "\n".join(out)
ids = list(nodes)
size = (len(ids) + nb - 1) // nb
Path("batches").mkdir(exist_ok=True)
for b in range(nb):
    chunk = ids[b*size:(b+1)*size]
    Path(f"batches/{tag}_{b+1}.txt").write_text("\n\n".join(render(nodes[i]) for i in chunk))
    print(f"batches/{tag}_{b+1}.txt", len(chunk))
