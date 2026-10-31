# Task: build a process ledger by reading sources one at a time, in rank order

Goal: a map of how a Romanian local social-assistance directorate (and the national payment agency AJPIS/ANPIS) runs the heating aid and energy supplement for vulnerable energy consumers (ajutorul pentru încălzirea locuinței și suplimentul pentru energie, Law 226/2021), that the directorate's own staff would confirm step by step.

Method (follow exactly):
1. Read the sources in the order listed (rank 1 first). Read each one completely before touching the next.
2. After source 1, write the ledger: a list of procedural CLAIMS ("actor A does X when T"), each with the sentence it rests on. No claim without a sentence. If the source does not name the actor, "who" = "unknown". If it does not say whether a step is automatic, "automation" = "unknown". Add "order" statements only where the text states order (words like "după", "în termen de", "ulterior", "la data", numbered steps, or statutory sequence). Record rules (conditions, amounts, deadlines) separately as rules, not as steps.
3. For each next source: read it, then update the ledger and append to the change log an entry {source, claims_added: [ids], claims_confirmed: [ids] (a second independent source states the same claim: record its quote too), claims_refined: [ids] (more detail, e.g. the actor or the deadline, now stated), contradictions: [{claim_id, what_this_source_says, quote}], rules_added, order_added}. A contradiction must stay visible; do not silently overwrite. Precedence rule for parameters (amounts, dates): the later-dated source wins but both values are kept; for structure (who does what, order): the norms (HG) and the law win over guidance; silence never loses to inference.
4. Rank order for this corpus (most procedural first): [1] the methodological norms HG 1073/2021 if present, [2] Law 226/2021, [3] the local directorate pages and notices, [4] the application form, [5] the national catalogue entry, [6] secondary explainers (press, guides). Lower ranks may add claims; mark such claims "low_rank_only": true until confirmed.
5. Write questions: every gap a process owner must answer (who decides, what the system does, what happens if ...).

Output (JSON, written to the path given):
{
 "sources_read": [{"rank": 1, "file": "...", "chars": n}],
 "steps": [{"id": "C01", "name": "...", "who": "citizen" | "das_staff" | "mayor" | "das_system" | "ajpis" | "supplier" | "other" | "unknown", "who_evidence": "", "automation": "automatic" | "manual" | "unknown", "what": "one sentence", "trigger": "", "sources": [{"file": "...", "quote": "verbatim, max 250 chars"}], "n_sources": n, "low_rank_only": false}],
 "order": [{"before": "C01", "after": "C02", "file": "...", "quote": "..."}],
 "rules": [{"id": "R01", "name": "...", "applies_in_step": "", "file": "...", "quote": "...", "values_by_source": []}],
 "contradictions": [{"claim_or_rule": "...", "a": {"file": "...", "quote": "..."}, "b": {"file": "...", "quote": "..."}, "resolution": "..."}],
 "change_log": [ {"source": "...", "rank": n, "claims_added": [], "claims_confirmed": [], "claims_refined": [], "contradictions": [], "rules_added": [], "order_added": []} ],
 "questions": [{"gap": "...", "where_it_would_matter": "C.."}]
}
Quotes verbatim (Romanian). Validate the JSON with python3. Reply with: the change-log counts per source (added / confirmed / refined / contradictions), the final counts (steps, order statements, rules, questions), and steps per "who".
