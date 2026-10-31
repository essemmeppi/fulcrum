"""Summarise alignment files: reference recall, generated precision, order agreement, overlap between runs."""
import json, glob, collections, itertools, sys
ref = {s["id"]: s for s in json.load(open("reference_steps_compact.json"))["steps"]}
files = sorted(glob.glob("outputs/align_*.json")) + sorted(glob.glob("/tmp/claude-0/-home-user-fulcrum/88c057c4-1cad-560c-8f42-792b69cd87c9/scratchpad/work/e2_kela/outputs/align_*.json"))
matched_sets = {}
rows = []
for f in files:
    d = json.load(open(f))
    r2g = d.get("reference_to_generated", [])
    matched = {x["ref_id"] for x in r2g if x.get("match_type") in ("exact", "partial", "merged")}
    exact = sum(1 for x in r2g if x.get("match_type") == "exact")
    gen_ids = set()
    for x in r2g:
        for n in x.get("matched_node_ids", []) or []: gen_ids.add(n)
    unmatched = d.get("generated_unmatched", [])
    gen_total = len(gen_ids | {u["node_id"] for u in unmatched})
    oc = d.get("order_checks", [])
    same = sum(1 for o in oc if o.get("same_order") is True); rev = sum(1 for o in oc if o.get("same_order") is False); nc = sum(1 for o in oc if o.get("same_order") == "not_connected")
    # acyclic variant if present
    same_ac = sum(1 for o in oc if o.get("same_order_acyclic") is True); has_ac = any("same_order_acyclic" in o for o in oc)
    by_sub = collections.defaultdict(lambda: [0, 0])
    for rid, s in ref.items():
        by_sub[s["subprocess"]][1] += 1
        if rid in matched: by_sub[s["subprocess"]][0] += 1
    name = f.split("/")[-1].replace("align_", "").replace(".json", "")
    matched_sets[name] = matched
    rows.append((name, len(matched), exact, len(gen_ids), gen_total, same, rev, nc, same_ac if has_ac else None, by_sub))
print(f"{'variant':34s} {'ref matched':>12s} {'exact':>5s} {'gen matched':>12s} {'order same/rev/nc':>18s}")
for name, m, ex, gm, gt, same, rev, nc, sac, by_sub in rows:
    print(f"{name:34s} {m:3d}/129 ({m/129:.2f}) {ex:5d} {gm:3d}/{gt:3d} ({gm/gt if gt else 0:.2f}) {same:3d}/{rev:2d}/{nc:2d}" + (f"  acyclic same={sac}" if sac is not None else ""))
print("\nrecall by subprocess (matched/total):")
subs = sorted({s["subprocess"] for s in ref.values()})
print(f"{'variant':34s} " + " ".join(f"{s[:10]:>10s}" for s in subs))
for name, m, ex, gm, gt, same, rev, nc, sac, by_sub in rows:
    print(f"{name:34s} " + " ".join(f"{by_sub[s][0]:3d}/{by_sub[s][1]:<3d}   " for s in subs))
print("\noverlap of matched reference steps between runs (Jaccard):")
for a, b in itertools.combinations(sorted(matched_sets), 2):
    A, B = matched_sets[a], matched_sets[b]
    if A and B: print(f"  {a:30s} {b:30s} {len(A & B) / len(A | B):.2f}")
