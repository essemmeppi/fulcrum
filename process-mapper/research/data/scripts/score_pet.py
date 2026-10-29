"""Score PET extraction outputs against gold.
Metrics:
  MD strict  : exact span (sid,start,end) match, per type (Activity, Actor)
  MD relaxed : predicted span overlaps a gold span of the same type (each gold matched at most once)
  Performer  : (activity, actor) pairs, relaxed matching of both ends
  Successor  : activity->activity direct successor pairs; gold derived by collapsing gateways/conditions
  Precedence : agreement on ordering relation (A<B, B<A, none, both) over pairs of gold activities that the model found
"""
import json, sys, itertools, collections
from pathlib import Path

def load_gold(p):
    return json.load(open(p))

def gold_successors(doc):
    ents = doc["entities"]
    head2ent = {(e["sid"], e["start"]): e for e in ents}
    adj = collections.defaultdict(list)
    for s_sid, s_tok, t_sid, t_tok in doc["flows"]:
        adj[(s_sid, s_tok)].append((t_sid, t_tok))
    acts = {(e["sid"], e["start"]) for e in ents if e["type"] == "Activity"}
    succ = set()
    for a in acts:
        # DFS through non-activity nodes
        stack = [n for n in adj[a]]; seen = set()
        while stack:
            n = stack.pop()
            if n in seen: continue
            seen.add(n)
            if n in acts:
                succ.add((a, n))
            else:
                stack.extend(adj[n])
    return succ, acts

def closure(pairs, nodes):
    reach = {n: set() for n in nodes}
    adj = collections.defaultdict(set)
    for a, b in pairs: adj[a].add(b)
    for n in nodes:
        stack = list(adj[n]); seen = set()
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x); stack.extend(adj[x])
        reach[n] = seen
    return reach

def overlap(a, b):
    return a["sid"] == b["sid"] and not (a["end"] < b["start"] or b["end"] < a["start"])

def match_spans(pred, gold):
    """Greedy one-to-one relaxed matching. Returns dict pred_index->gold_index."""
    used = set(); m = {}
    for i, p in enumerate(pred):
        for j, g in enumerate(gold):
            if j in used: continue
            if overlap(p, g):
                m[i] = j; used.add(j); break
    return m

def prf(tp, npred, ngold):
    P = tp / npred if npred else 0.0
    R = tp / ngold if ngold else 0.0
    F = 2 * P * R / (P + R) if P + R else 0.0
    return P, R, F

def score(gold, out_dir, docs):
    tot = collections.Counter()
    prec_agree = prec_total = 0
    per_doc = {}
    missing = []
    for name in docs:
        p = Path(out_dir) / f"{name}.json"
        if not p.exists():
            missing.append(name); continue
        try:
            pred = json.load(open(p))
        except Exception as e:
            missing.append(name + " (invalid json)"); continue
        g = gold[name]
        g_act = [e for e in g["entities"] if e["type"] == "Activity"]
        g_actor = [e for e in g["entities"] if e["type"] == "Actor"]
        p_act = [dict(a) for a in pred.get("activities", [])]
        p_actor = [dict(a) for a in pred.get("actors", [])]
        for lst in (p_act, p_actor):
            for a in lst:
                a.setdefault("end", a["start"])
        # strict
        gs_act = {(e["sid"], e["start"], e["end"]) for e in g_act}
        gs_actor = {(e["sid"], e["start"], e["end"]) for e in g_actor}
        tot["act_strict_tp"] += len({(a["sid"], a["start"], a["end"]) for a in p_act} & gs_act)
        tot["actor_strict_tp"] += len({(a["sid"], a["start"], a["end"]) for a in p_actor} & gs_actor)
        tot["act_pred"] += len(p_act); tot["act_gold"] += len(g_act)
        tot["actor_pred"] += len(p_actor); tot["actor_gold"] += len(g_actor)
        # relaxed
        m_act = match_spans(p_act, g_act); m_actor = match_spans(p_actor, g_actor)
        tot["act_relaxed_tp"] += len(m_act); tot["actor_relaxed_tp"] += len(m_actor)
        # maps from predicted head -> gold head
        pa2g = {(p_act[i]["sid"], p_act[i]["start"]): (g_act[j]["sid"], g_act[j]["start"]) for i, j in m_act.items()}
        pac2g = {(p_actor[i]["sid"], p_actor[i]["start"]): (g_actor[j]["sid"], g_actor[j]["start"]) for i, j in m_actor.items()}
        # performers
        g_perf = {((s, st), (t, tt)) for s, st, t, tt in g["performers"]}
        p_perf = set()
        for r in pred.get("performers", []):
            a = tuple(r["activity"]); b = tuple(r["actor"])
            if a in pa2g and b in pac2g:
                p_perf.add((pa2g[a], pac2g[b]))
            else:
                p_perf.add((("x",) + a, ("x",) + b))  # unmatched -> counts as false positive
        tot["perf_tp"] += len(p_perf & g_perf); tot["perf_pred"] += len(pred.get("performers", [])); tot["perf_gold"] += len(g_perf)
        # successors
        g_succ, g_acts = gold_successors(g)
        p_succ_raw = [(tuple(r["from"]), tuple(r["to"])) for r in pred.get("successors", [])]
        p_succ = set()
        for a, b in p_succ_raw:
            if a in pa2g and b in pa2g and pa2g[a] != pa2g[b]:
                p_succ.add((pa2g[a], pa2g[b]))
            else:
                p_succ.add((("x",) + a, ("x",) + b))
        tot["succ_tp"] += len(p_succ & g_succ); tot["succ_pred"] += len(p_succ_raw); tot["succ_gold"] += len(g_succ)
        # precedence agreement over gold activities the model found
        found = sorted(set(pa2g.values()))
        g_reach = closure(g_succ, g_acts)
        p_pairs = {(a, b) for a, b in p_succ if a in g_acts and b in g_acts}
        p_reach = closure(p_pairs, set(found))
        def rel(reach, a, b):
            ab = b in reach.get(a, set()); ba = a in reach.get(b, set())
            return (ab, ba)
        agree = total = 0
        for a, b in itertools.combinations(found, 2):
            total += 1
            if rel(g_reach, a, b) == rel(p_reach, a, b): agree += 1
        prec_agree += agree; prec_total += total
        # ordered pairs (A strictly before B) restricted to activities the model found
        g_ord = {(a, b) for a in found for b in found if a != b and b in g_reach.get(a, set()) and a not in g_reach.get(b, set())}
        p_ord = {(a, b) for a in found for b in found if a != b and b in p_reach.get(a, set()) and a not in p_reach.get(b, set())}
        tot["ord_tp"] += len(g_ord & p_ord); tot["ord_pred"] += len(p_ord); tot["ord_gold"] += len(g_ord)
        tot["ord_reversed"] += len({(b, a) for a, b in g_ord} & p_ord)
        per_doc[name] = {"act_F1_relaxed": prf(len(m_act), len(p_act), len(g_act))[2], "succ_F1": prf(len(p_succ & g_succ), len(p_succ_raw), len(g_succ))[2], "prec_agree": agree / total if total else None}
    res = {
        "docs_scored": len(per_doc), "missing": missing,
        "activity_strict": prf(tot["act_strict_tp"], tot["act_pred"], tot["act_gold"]),
        "activity_relaxed": prf(tot["act_relaxed_tp"], tot["act_pred"], tot["act_gold"]),
        "actor_strict": prf(tot["actor_strict_tp"], tot["actor_pred"], tot["actor_gold"]),
        "actor_relaxed": prf(tot["actor_relaxed_tp"], tot["actor_pred"], tot["actor_gold"]),
        "performer": prf(tot["perf_tp"], tot["perf_pred"], tot["perf_gold"]),
        "successor": prf(tot["succ_tp"], tot["succ_pred"], tot["succ_gold"]),
        "precedence_agreement": prec_agree / prec_total if prec_total else None,
        "ordered_pairs": prf(tot["ord_tp"], tot["ord_pred"], tot["ord_gold"]),
        "ordered_pairs_reversed_share_of_gold": tot["ord_reversed"] / tot["ord_gold"] if tot["ord_gold"] else None,
        "precedence_pairs": prec_total,
        "counts": dict(tot),
    }
    return res, per_doc

if __name__ == "__main__":
    gold = load_gold(sys.argv[1]); out_dir = sys.argv[2]
    docs = [l.strip().replace(".txt", "") for l in open(sys.argv[3]) if l.strip()]
    res, per_doc = score(gold, out_dir, docs)
    for k, v in res.items():
        if isinstance(v, tuple): print(f"{k:22s} P={v[0]:.3f} R={v[1]:.3f} F1={v[2]:.3f}")
        else: print(f"{k:22s} {v}")
    json.dump({"summary": res, "per_doc": per_doc}, open(Path(out_dir) / "_scores.json", "w"), indent=1)
