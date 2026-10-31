# Task: reconstruct the administrative process of Australia's Rent Assistance from public documents

You are a public-administration process analyst. Read the PUBLIC document files listed below (they are the ONLY sources you may use; do not use outside knowledge of Centrelink / Services Australia) and reconstruct the end-to-end administrative process by which Services Australia assesses, pays, verifies and reviews Rent Assistance (RA), as a process map that lists every step, who does it, and the order of steps.

## What to produce
One JSON object with:
- "actors": [{"id": "customer" | "sa_staff" | "sa_system" | "landlord_or_agent" | "other", "name": "...", "kind": "citizen" | "caseworker" | "system" | "third_party" | "other_authority"}]
- "nodes": the steps, from the triggering event to the end states, covering: claim or circumstance update that triggers assessment, eligibility checks (eligible payment, accommodation type, rent threshold, special rules), rent verification (what proof, how it is requested and processed, what happens if not provided), rate calculation, payment, change of circumstances, periodic review, travel, cancellation. Each node:
  {"id": "N01", "name": "short name", "description": "one sentence", "type": "start_event" | "end_event" | "citizen_task" | "caseworker_task" | "system_task" | "third_party_task" | "decision" | "wait" | "timer", "actor_id": "...", "visibility": "external" (customer sees/does it) | "internal" (inside the agency), "automation_class": "citizen_action" | "deterministic_rule" | "register_lookup" | "document_check" | "judgment" | "human_signoff" | "notification", "agent_mode": "agent_can_execute" | "agent_prepares_human_decides" | "human_only", "confidence": 0-1 (0.9+ stated explicitly in two or more sources; 0.7-0.89 stated explicitly in one source; 0.5-0.69 implied; below 0.5 inferred from general practice), "evidence": [{"source": "<file name>", "quote": "verbatim passage, max 250 chars"}] (empty if inferred), "inferred_reason": "" or why you added it without evidence}
- "edges": [{"source": "N01", "target": "N02", "condition": "" or the condition on this path when leaving a decision}]

## Quality bar
- One node = one unit of work by one actor. Do not collapse distinct steps; do not pad. Include internal steps when a document implies them, with honest confidence, and mark inferred steps clearly (empty evidence + inferred_reason). Quotes must be verbatim from the files.
- Every node except end events has at least one outgoing edge; every node except start events at least one incoming edge.

## Procedure
Read every file in inputs_public/ completely. Write the JSON to the output path given. Validate it parses with python3 and that all edge endpoints exist. Reply with: number of nodes, edges, nodes per actor, and 3 steps you were least sure about.
