"""E4: how much ordering information does each public document carry?
For each source document, order the map's nodes by the position of their earliest provenance quote in that
document; compare with the node's position in the process (depth on the main flow). Kendall's tau per document."""
import json, re, unicodedata, collections, itertools
from pathlib import Path
MAP = json.load(open("/home/user/fulcrum/process-mapper/maps/fi-kela-general-housing-allowance/map.json"))
CORPUS = Path("/home/user/fulcrum/process-mapper/corpus/fi-kela-general-housing-allowance")
def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("–","-").replace("—","-")
    return re.sub(r"\s+"," ",s).strip().lower()
texts = {p.stem: norm(p.read_text()) for p in CORPUS.glob("*.txt")}
# process depth: BFS from start events over edges, ignoring edges into already-visited nodes (breaks cycles)
nodes = {n["id"]: n for n in MAP["nodes"]}
adj = collections.defaultdict(list)
for e in MAP["edges"]: adj[e["source"]].append(e["target"])
depth = {}
starts = [n["id"] for n in MAP["nodes"] if n["type"] == "start_event"]
# main flow first (S_APPLY), then other starts so their depths come after the main chain
order_starts = ["S_APPLY"] + [s for s in starts if s != "S_APPLY"]
from collections import deque
d0 = 0
for s in order_starts:
    if s in depth: continue
    q = deque([(s, d0)])
    while q:
        n, d = q.popleft()
        if n in depth: continue
        depth[n] = d
        for t in adj[n]: q.append((t, d + 1))
    d0 = max(depth.values()) + 1
# earliest quote position per node per source
pos = collections.defaultdict(dict)  # source -> node -> min offset
for n in MAP["nodes"]:
    for p in n["provenance"]:
        src = p["source_id"]; q = norm(p["quote"])
        frags = [f for f in re.split(r"\s*(?:\.\.\.|…)\s*", q) if f]
        if not frags or src not in texts: continue
        i = texts[src].find(frags[0])
        if i >= 0:
            pos[src][n["id"]] = min(pos[src].get(n["id"], 1e12), i)
def kendall(pairs):
    c = dcount = 0
    for (a1, b1), (a2, b2) in itertools.combinations(pairs, 2):
        s = (a1 - a2) * (b1 - b2)
        if s > 0: c += 1
        elif s < 0: dcount += 1
    return (c - dcount) / (c + dcount) if c + dcount else None, c + dcount
print(f"{'source':38s} {'nodes':>5s} {'tau':>6s} {'pairs':>6s}  main-flow-only tau (nodes)")
rows = []
for src, d in sorted(pos.items(), key=lambda kv: -len(kv[1])):
    pairs = [(d[n], depth.get(n, 999)) for n in d if n in depth]
    tau, npairs = kendall(pairs)
    main = [(d[n], depth[n]) for n in d if n in depth and depth[n] < 40]
    tau_m, _ = kendall(main)
    rows.append({"source": src, "nodes_with_quotes": len(d), "tau_all": tau, "pairs": npairs, "tau_main_flow": tau_m, "main_nodes": len(main)})
    print(f"{src:38s} {len(d):5d} {tau if tau is not None else float('nan'):6.2f} {npairs:6d}  {tau_m if tau_m is not None else float('nan'):6.2f} ({len(main)})")
json.dump({"depth": depth, "rows": rows}, open("order_stats.json", "w"), indent=1)
print("\nmain-flow depth cutoff 40; depth of key nodes:", {k: depth.get(k) for k in ["S_APPLY","T_SUBMIT_APP","T_REGISTER","T_CALC","T_DECIDE","T_NOTIFY","T_PAY_APPLICANT","S_CHANGE","S_ANNUAL","S_DISSATISFIED"]})
