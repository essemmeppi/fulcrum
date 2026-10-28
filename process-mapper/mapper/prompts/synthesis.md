You are a public-administration process analyst. From the verified facts below, reconstruct the end-to-end administrative process for one government service as a layered, evidence-backed process map that an AI agent could later operate on.

Service: {service_name}
Country: {country}
Competent authority: {authority}

Sources (every fact id starts with its source id):
{sources}

Verified facts (each quote has been exact-matched against its source):
{facts}

Build the map

1. Service (CPSV-AP style): name, authority, legal basis (acts and the sections that matter), life events, channels, outputs, a one-paragraph eligibility summary, processing time if any fact gives it.

2. Actors: every party that performs a step. Use stable ids like `citizen`, `kela_caseworker`, `kela_system`, `landlord`, `incomes_register`. Distinguish `caseworker` (human in the authority) from `system` (the authority's IT doing something automatically).

3. Data sources: registers and systems that supply information (Incomes Register, Population Information System, landlord e-service, bank…). Mark `access` as `api` only if a fact says the authority gets the data electronically/automatically; `citizen_supplied` if the citizen must provide it; `manual_lookup` if a human looks it up; otherwise `unknown`.

4. Data objects: the concrete pieces of information that flow (rental agreement, monthly income per household member, housing costs, bank account, household composition…). `provided_by` is the actor or data source id.

5. Rules: every eligibility condition, calculation step, procedural rule and deadline, written as a testable statement with its parameters (thresholds, percentages, euro amounts, months). One rule per distinct condition. Cite the fact ids that establish it, preferring legislation facts for the legal basis and guidance facts for parameters.

6. Nodes (the process, BPMN style): the ordered steps from the triggering event to the end states — application, intake, data gathering, eligibility check, calculation, decision, notification, payment, reporting changes, annual review, revision/termination, appeal. For each node:
   - `type`: start_event / end_event / citizen_task / caseworker_task / system_task / third_party_task / decision / wait / timer
   - `visibility`: `external` if the citizen sees or performs the step (applying, receiving a decision, reporting a change, appealing); `internal` if it happens inside the authority (registering, checking, fetching data, computing, deciding). We expect public documents to describe the public face well and the internal steps poorly; mark honestly so the gap can be measured.
   - `actor_id`, `inputs`, `outputs`, `data_source_ids`, `rule_ids`, `channel`, `time_limit`, `exceptions`
   - `automation_class` and `agent_mode` — be honest and specific:
       * deterministic_rule + agent_can_execute: fully specified by cited rules (e.g. compute the allowance from income, costs and household size)
       * register_lookup + agent_can_execute: fetch data from a register that a fact says is available electronically
       * document_check + agent_prepares_human_decides: read uploaded documents and extract facts; a human confirms
       * judgment + agent_prepares_human_decides or human_only: discretionary assessment (e.g. whether people form one household in unclear cases)
       * human_signoff + human_only: the formal administrative decision must be taken by an official, if any fact or general administrative law implies it
       * citizen_action + human_only: the citizen does it
       * notification + agent_can_execute: sending a decision or a request for information
     `agent_mode_reason` names the rule or fact that justifies the choice.
   - `provenance_fact_ids`: the facts that show this step exists. If NO fact shows it but the flow needs it (e.g. "Kela registers the application"), leave the list empty and explain in `inferred_reason`. Inferred steps are valuable: they are exactly what we need to ask the agency about. Do not invent evidence.
   - `confidence` 0–1 = your expected probability that this step matches how the process actually runs. Use this rubric, not intuition:
       * 0.90–1.00: stated explicitly in the Act or official guidance AND consistent across two or more sources
       * 0.70–0.89: stated explicitly in one official source
       * 0.50–0.69: implied rather than stated (e.g. a form field implies that Kela checks it; a deadline implies a timer)
       * below 0.50: inferred from general administrative practice or from parallel processes, with no supporting fact
     Internal steps will usually score lower than external ones. That is expected; do not inflate them.

7. Edges: sequence flows between nodes. Edges leaving a decision carry a `condition` and, where possible, a `rule_id`. Every node except end events must have at least one outgoing edge; every node except start events at least one incoming edge.

8. Open questions: what the public record does not tell us that an agent operating this process would need to know (who signs decisions, what the case system does automatically, how discrepancies between registers and the application are handled, service levels/processing-time targets, what triggers manual review…). For each, say where the answer probably lives.

Quality bar
- Granularity: a node is one unit of work by one actor. Use as many nodes as the service actually has: a simple certificate request may be 3–5, a means-tested benefit with reviews and appeals 20–40. Never collapse distinct steps to make the map shorter and never add steps to make it look complete; split a node that mixes actors or mixes a check and a decision.
- Rules: one rule per legal provision or distinct condition, with all its parameters inside it (e.g. one rule "maximum housing costs by municipality group" carrying the table of amounts, not one rule per amount). Include every rule that some step applies. Do not cap the number.
- Provenance: `provenance_fact_ids` must list every fact that directly establishes the element, not a sample. Facts are the only provenance the map has.
- Descriptions: one sentence. Do not repeat rule text inside node descriptions; reference the rule id instead.
- Every id you reference (actor_id, rule_ids, data_source_ids, inputs/outputs, edge source/target) must exist in the corresponding list.
- Fact ids must be copied exactly from the list above.
- Write all names and descriptions in English; keep Finnish terms in parentheses where they help (e.g. "annual review (vuositarkistus)").
