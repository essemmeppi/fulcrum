"""Prepare PET documents for extraction and a gold file for scoring.
Gold: activities, actors, flow relations (head token ids) per document."""
import json, re, sys
from pathlib import Path
D = Path(sys.argv[1]); OUT = Path(sys.argv[2])
rel = json.load(open(D/"PETv1.1-relations.json"))
docs = {}
for d in rel:
    name = d["document name"]
    toks, sids, tids, tags = d["tokens"], d["sentence-IDs"], d["tokens-IDs"], d["ner_tags"]
    # entities: spans (sid, start_tid, end_tid, type)
    ents = []
    cur = None
    for i,(t,s,tid,tag) in enumerate(zip(toks,sids,tids,tags)):
        if tag.startswith("B-"):
            if cur: ents.append(cur)
            cur = {"sid":s,"start":tid,"end":tid,"type":tag[2:],"text":t}
        elif tag.startswith("I-") and cur and cur["sid"]==s and tag[2:]==cur["type"]:
            cur["end"]=tid; cur["text"]+=" "+t
        else:
            if cur: ents.append(cur); cur=None
    if cur: ents.append(cur)
    flows = [(r["source-head-sentence-ID"], r["source-head-word-ID"], r["target-head-sentence-ID"], r["target-head-word-ID"]) for r in d["relations"] if r["relation-type"]=="flow"]
    performers = [(r["source-head-sentence-ID"], r["source-head-word-ID"], r["target-head-sentence-ID"], r["target-head-word-ID"]) for r in d["relations"] if r["relation-type"]=="actor performer"]
    # sentences
    sents = {}
    for t,s,tid in zip(toks,sids,tids):
        sents.setdefault(s,[]).append((tid,t))
    docs[name] = {"entities":ents, "flows":flows, "performers":performers, "sentences":{s:[t for _,t in sorted(v)] for s,v in sents.items()}}
json.dump(docs, open(OUT/"gold.json","w"), indent=1)
# input rendering: numbered sentences and tokens
for name,doc in docs.items():
    lines=[]
    for s in sorted(doc["sentences"]):
        toks=doc["sentences"][s]
        lines.append(f"S{s}: " + " ".join(f"{t}[{i}]" for i,t in enumerate(toks)))
    (OUT/"inputs"/f"{name}.txt").write_text("\n".join(lines))
print(len(docs),"docs")
import collections
c=collections.Counter(e["type"] for d in docs.values() for e in d["entities"])
print("entities by type", dict(c))
print("flows", sum(len(d["flows"]) for d in docs.values()), "performers", sum(len(d["performers"]) for d in docs.values()))
print("sentences", sum(len(d["sentences"]) for d in docs.values()))
