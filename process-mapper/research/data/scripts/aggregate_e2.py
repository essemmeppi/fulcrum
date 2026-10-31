"""Aggregate node-verification outputs: verdict distributions, judge agreement, calibration, breakdowns."""
import json, glob, collections, itertools, sys
from pathlib import Path
MAP = json.load(open("/home/user/fulcrum/process-mapper/maps/fi-kela-general-housing-allowance/map.json"))
nodes = {n["id"]: n for n in MAP["nodes"]}
def load(model):
    out = {}
    for p in sorted(glob.glob(f"outputs/verify_{model}_[0-9].json")):
        for r in json.load(open(p)):
            out[r["node_id"]] = r
    return out
def collapse(v):
    # three-way: supported (step or with corrections or rule-only), absent, contradicted
    return {"confirmed_step": "exists", "confirmed_with_corrections": "exists", "confirmed_rule_only": "rule_only",
            "not_mentioned": "absent", "contradicted": "contradicted"}.get(v, v)
def kappa(a, b, keys):
    pairs = [(a[k], b[k]) for k in keys]
    n = len(pairs)
    po = sum(x == y for x, y in pairs) / n
    ca = collections.Counter(x for x, _ in pairs); cb = collections.Counter(y for _, y in pairs)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po
def main():
    models = [m for m in ("opus", "sonnet") if glob.glob(f"outputs/verify_{m}_[0-9].json")]
    res = {m: load(m) for m in models}
    for m in models:
        r = res[m]
        print(f"\n== {m}: {len(r)} nodes reviewed ==")
        print(" verdicts:", dict(collections.Counter(x["verdict"] for x in r.values())))
        print(" actor_check:", dict(collections.Counter(x.get("actor_check") for x in r.values())))
        print(" automation_check:", dict(collections.Counter(x.get("automation_check") for x in r.values())))
        print(" order_check:", dict(collections.Counter(x.get("order_check") for x in r.values())))
        print(" granularity:", dict(collections.Counter(x.get("granularity") for x in r.values())))
        # breakdowns
        for key, fn in [("visibility", lambda n: n["visibility"]), ("n_sources", lambda n: "1 source" if len(set(f.split(":")[0] for f in n["provenance_fact_ids"])) <= 1 else "2+ sources"),
                        ("automation_class", lambda n: n["automation_class"]), ("conf_bin", lambda n: "<0.7" if n["confidence"] < 0.7 else ("0.7-0.89" if n["confidence"] < 0.9 else ">=0.9"))]:
            tab = collections.defaultdict(collections.Counter)
            for nid, x in r.items():
                tab[fn(nodes[nid])][collapse(x["verdict"])] += 1
            print(f" by {key}:")
            for k, c in sorted(tab.items()):
                tot = sum(c.values())
                print(f"   {k:18s} n={tot:2d}  exists={c['exists']/tot:.2f} rule_only={c['rule_only']/tot:.2f} absent={c['absent']/tot:.2f} contradicted={c['contradicted']/tot:.2f}")
        # exact verdict by confidence (calibration): share 'exists or rule_only' vs model confidence
        import statistics
        for lab, pred in [("exists", lambda v: collapse(v) == "exists"), ("exists_or_rule", lambda v: collapse(v) in ("exists", "rule_only"))]:
            bins = collections.defaultdict(list)
            for nid, x in r.items():
                c = nodes[nid]["confidence"]
                b = "<0.6" if c < 0.6 else "0.6-0.69" if c < 0.7 else "0.7-0.79" if c < 0.8 else "0.8-0.89" if c < 0.9 else ">=0.9"
                bins[b].append(pred(x["verdict"]))
            print(f" calibration ({lab}):", {b: f"{sum(v)/len(v):.2f} (n={len(v)})" for b, v in sorted(bins.items())})
    if len(models) == 2:
        keys = sorted(set(res["opus"]) & set(res["sonnet"]))
        a = {k: res["opus"][k]["verdict"] for k in keys}; b = {k: res["sonnet"][k]["verdict"] for k in keys}
        k5, po5 = kappa(a, b, keys)
        a3 = {k: collapse(v) for k, v in a.items()}; b3 = {k: collapse(v) for k, v in b.items()}
        k3, po3 = kappa(a3, b3, keys)
        print(f"\n== judge agreement on {len(keys)} nodes: 5-way kappa={k5:.2f} (raw {po5:.2f}); 3-way (exists/rule_only/absent/contradicted) kappa={k3:.2f} (raw {po3:.2f})")
        dis = [(k, a[k], b[k]) for k in keys if a3[k] != b3[k]]
        print(" disagreements (collapsed):", dis)
        # consensus table
        cons = collections.Counter()
        for k in keys:
            cons[(a3[k], b3[k])] += 1
        print(" cross-tab (opus, sonnet):", dict(cons))
if __name__ == "__main__":
    main()
