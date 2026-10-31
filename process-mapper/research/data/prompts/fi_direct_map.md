# Task: reconstruct the administrative process of one public service from documents

You are a public-administration process analyst. Read the document files listed below (they are the ONLY sources you may use; do not use outside knowledge of Kela) and reconstruct the end-to-end administrative process of Finland's general housing allowance (yleinen asumistuki), administered by Kela, as a process map that lists every step, who does it, and the order of steps.

## What to produce
One JSON object with:
- "actors": [{"id": "citizen" | "kela_caseworker" | "kela_system" | "landlord" | "other_authority" | <other short id>, "name": "...", "kind": "citizen" | "caseworker" | "system" | "third_party" | "other_authority"}]
- "nodes": the steps, from the triggering event to the end states, covering: application, intake/registration, data gathering from registers, eligibility checks, calculation, decision, notification, payment, reporting changes, mid-period revision, annual review, termination, overpayment recovery, appeal. Each node:
  {"id": "N01", "name": "short English name", "description": "one sentence", "type": "start_event" | "end_event" | "citizen_task" | "caseworker_task" | "system_task" | "third_party_task" | "decision" | "wait" | "timer", "actor_id": "...", "visibility": "external" (citizen sees/does it) | "internal" (inside the authority), "automation_class": "citizen_action" | "deterministic_rule" | "register_lookup" | "document_check" | "judgment" | "human_signoff" | "notification", "agent_mode": "agent_can_execute" | "agent_prepares_human_decides" | "human_only", "confidence": 0-1 (your expected probability that this step matches how the process actually runs: 0.9+ stated explicitly in two or more sources; 0.7-0.89 stated explicitly in one source; 0.5-0.69 implied; below 0.5 inferred from general practice), "evidence": [{"source": "<file name>", "quote": "verbatim passage, max 250 chars, original language"}] (empty list if inferred), "inferred_reason": "" or why you added it without evidence}
- "edges": [{"source": "N01", "target": "N02", "condition": "" or the condition on this path when leaving a decision}]

## Quality bar
- One node = one unit of work by one actor. Do not collapse distinct steps; do not pad. A means-tested benefit with reviews and appeals typically has 30-90 nodes. Split a node that mixes actors or mixes a check and a decision.
- Every node except end events has at least one outgoing edge; every node except start events has at least one incoming edge.
- Internal steps (what happens inside Kela) must be included when a document implies them, with honest confidence. Mark inferred steps clearly (empty evidence + inferred_reason). Do not invent evidence; quotes must be verbatim from the files.
- Names and descriptions in English; keep Finnish terms in parentheses where useful.

## Procedure
Read every listed file completely (use Read with offset/limit for long files). Then write the JSON to the output path given. Validate it parses with python3 and that all edge endpoints exist in nodes. Reply with: number of nodes, edges, nodes per actor, and 3 steps you were least sure about.
