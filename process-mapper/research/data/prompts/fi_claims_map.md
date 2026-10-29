# Task: a process map that says only what the documents say

Goal: a map of Finland's general housing allowance process that a Kela process owner would confirm step by step. The map is a list of procedural CLAIMS, each tied to a sentence. Rule: no claim without a sentence. If the documents do not say who does a step, the actor is "unknown". If they do not say whether it is automatic, automation is "unknown". If they do not say what comes next, there is no edge. A rule (a condition, an amount) is not a step; record it as a rule, not as a node. Do not add steps "the flow needs"; instead write the gap as a question.

Read the listed files completely (Read with offset/limit for long files). They are the ONLY sources.

Output JSON:
{
 "steps": [{"id": "C01", "name": "short English name", "who": "citizen" | "kela_staff" | "kela_system" | "landlord" | "other_authority" | "unknown", "who_evidence": "the words that name the actor, or ''", "automation": "automatic" | "manual" | "unknown", "automation_evidence": "", "what": "one sentence", "trigger": "what starts this step, as stated, or ''", "source": "<file>", "quote": "verbatim, max 250 chars"}],
 "order": [{"before": "C01", "after": "C02", "source": "<file>", "quote": "the sentence that states the order (words like 'after', 'then', 'when', 'before', a numbered sequence, or statutory sequence), max 250 chars"}],
 "rules": [{"id": "R01", "name": "...", "applies_in_step": "C.. or ''", "source": "...", "quote": "..."}],
 "questions": [{"gap": "what the documents do not say that a process owner must answer", "where_it_would_matter": "C.."}]
}
Quality bar: every quote verbatim; every step id in "order" exists; aim for every procedural sentence in the documents to become a step, and nothing else to become a step. Expect 25-60 steps and 15-40 order statements. Validate the JSON with python3. Reply with: steps, order statements, rules, questions, and steps per "who".
