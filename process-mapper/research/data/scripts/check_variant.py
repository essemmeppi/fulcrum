"""Structural stats and evidence verification for a variant map JSON.
Evidence quote is 'verified' if it appears verbatim (normalised) in the named source file."""
import json, re, sys, unicodedata, collections
from pathlib import Path
IN = Path(__file__).parent / "inputs"
def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("–","-").replace("—","-")
    return re.sub(r"\s+"," ",s).strip().lower()
texts = {p.name: norm(p.read_text()) for p in IN.glob("*.txt")}
def check(path):
    m = json.load(open(path))
    nodes = m.get("nodes", []); edges = m.get("edges", [])
    ids = {n["id"] for n in nodes}
    dangling = [e for e in edges if e.get("source") not in ids or e.get("target") not in ids]
    q_total = q_ok = q_badsrc = 0
    nodes_with_ev = 0
    for n in nodes:
        ev = n.get("evidence") or []
        if ev: nodes_with_ev += 1
        for e in ev:
            q_total += 1
            src = e.get("source","")
            src = src if src in texts else next((k for k in texts if k.startswith(src.replace(".txt",""))), None)
            if not src: q_badsrc += 1; continue
            frags = [f for f in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", norm(e.get("quote",""))) if f]
            pos, good = 0, bool(frags)
            for f in frags:
                i = texts[src].find(f, pos)
                if i < 0: good = False; break
                pos = i + len(f)
            q_ok += good
    conf = [n.get("confidence") for n in nodes if isinstance(n.get("confidence"), (int,float))]
    return {
        "file": Path(path).name, "nodes": len(nodes), "edges": len(edges), "dangling_edges": len(dangling),
        "actors": dict(collections.Counter(n.get("actor_id") for n in nodes)),
        "visibility": dict(collections.Counter(n.get("visibility") for n in nodes)),
        "types": dict(collections.Counter(n.get("type") for n in nodes)),
        "agent_mode": dict(collections.Counter(n.get("agent_mode") for n in nodes)),
        "nodes_with_evidence": nodes_with_ev, "quotes": q_total, "quotes_verified": q_ok, "quotes_bad_source": q_badsrc,
        "quote_verified_rate": round(q_ok / q_total, 3) if q_total else None,
        "mean_confidence": round(sum(conf)/len(conf), 3) if conf else None,
    }
if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(check(p), ensure_ascii=False))
