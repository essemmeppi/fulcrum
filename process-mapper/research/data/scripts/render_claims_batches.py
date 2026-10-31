"""Render the claims-only map into verification batches (same batch format as other variants)."""
import json, sys
from pathlib import Path
m = json.load(open(sys.argv[1])); tag = sys.argv[2]; nb = int(sys.argv[3])
steps = {s["id"]: s for s in m["steps"]}
before, after = {}, {}
for o in m.get("order", []):
    after.setdefault(o["before"], []).append(o["after"]); before.setdefault(o["after"], []).append(o["before"])
def render(s):
    out = [f"NODE {s['id']}", f"  name: {s['name']}", f"  description: {s.get('what','')}",
           f"  type: task; actor: {s.get('who')} (actor evidence: {s.get('who_evidence','')!r}); visibility: n/a",
           f"  automation_class: {s.get('automation')} (automation evidence: {s.get('automation_evidence','')!r}); agent_mode: n/a; confidence (model's own): n/a",
           f"  trigger: {s.get('trigger','')}"]
    out.append("  predecessors: " + ("; ".join(f"{p} ({steps[p]['name']})" for p in before.get(s["id"], []) if p in steps) or "none (no order statement in the documents)"))
    out.append("  successors: " + ("; ".join(f"{p} ({steps[p]['name']})" for p in after.get(s["id"], []) if p in steps) or "none (no order statement in the documents)"))
    out.append(f"  public-source evidence: 1 quote from {s.get('source')}")
    return "\n".join(out)
ids = list(steps); size = (len(ids) + nb - 1) // nb
for b in range(nb):
    chunk = ids[b*size:(b+1)*size]
    Path(f"batches/{tag}_{b+1}.txt").write_text("\n\n".join(render(steps[i]) for i in chunk)); print(f"batches/{tag}_{b+1}.txt", len(chunk))
# also a nodes/edges view for the alignment prompt
nodes = [{"id": s["id"], "name": s["name"], "description": s.get("what",""), "actor_id": s.get("who"), "type": "task"} for s in m["steps"]]
edges = [{"source": o["before"], "target": o["after"], "condition": ""} for o in m.get("order", [])]
json.dump({"nodes": nodes, "edges": edges}, open(sys.argv[1].replace(".json", "_as_map.json"), "w"), ensure_ascii=False, indent=1)
print("as_map written")
