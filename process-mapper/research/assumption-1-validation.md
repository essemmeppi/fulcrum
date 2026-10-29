# Can documents give a process map the agency will sign?

Validation of assumption 1. October 2026. Three countries, three kinds of reference, one question: when a model reads an agency's documents and draws the process, does the agency's own record say "yes, this is what we do"?

## The answer in five lines

1. **Steps: yes, with corrections.** Finland, 84-step map from public documents, checked step by step against Kela's internal staff guidelines by two independent judges: 0 to 1 step contradicted, 5 absent, 45 confirmed as steps, 21 confirmed as rules. Australia and Germany give the same picture.
2. **Order: direction is right, links are missing.** Reversed order is rare (under 1 per cent of pairs on the benchmark, 3 of 84 steps in Finland). The errors are missing and extra links, and triggers that start a branch at the wrong point.
3. **Actors and automation: not from public documents.** The maps call 30 to 50 per cent of steps "system". The staff guideline confirms 5 of 29, gives 5 to a caseworker, and is silent on 19. This is where "synthesis without reality" shows: the model fills a field the documents never answer.
4. **Coverage: half.** Public documents recover 40 to 58 per cent of the steps the staff guideline describes. What they miss is uniform across countries: case-by-case data gathering, internal routing, exception handling.
5. **The lever is not the pipeline shape.** Two-pass and single-pass, three models, give the same error profile. What moves the result: which documents are read (the law and the staff guide carry the order; forms carry none), whether a step has two independent sources (four times the confirmation rate), and whether the pipeline is allowed to invent actors and order.

## 1. What was tested

| Country, service | Built from | Checked against | Why this reference |
|---|---|---|---|
| Finland, general housing allowance (Kela) | 7 public documents: Act, 4 guidance pages and PDFs, form, service catalogue (170k chars) | Kela's staff benefit guideline (83 pages, "primarily for internal use", published as PDF) plus 3 cross-benefit staff guidelines (appeals, recovery, correction; 118 pages) | What the agency tells its own staff |
| Australia, Rent Assistance (Services Australia) | 19 public pages and factsheets (40k chars) | Operational Blueprint: 8 staff procedure pages with numbered step tables (200k chars) | Screen-level staff procedure |
| Germany, residence permit on humanitarian grounds | Statute text only: 17 sections of the Residence Act, 7 of the Administrative Procedure Act (78k chars) | The federal FIM reference process model (42 activity groups with legal bases, government-authored) | The government's own process model |

Plus the standard academic benchmark (PET, 45 annotated process descriptions) to show the reading step itself works.

**Method, in one paragraph.** Maps were built by Claude agents (Haiku, Sonnet, Opus 5.5) from the public documents only; no builder saw a reference. Each step of a map was then given one of five verdicts by a judge that read the whole reference: *described as a step* (who does what), *step exists but a detail differs* (actor, automation, trigger, order, granularity), *only the rule is stated*, *contradicted*, *not mentioned*. Every quote a judge cited was checked by code against the reference text (357 of 357 verbatim in the Finnish round). Two judges (Opus, Sonnet) rated the Finnish map independently: kappa 0.70. Recall was measured the other way round: an agent wrote the process from the staff guideline alone (129 steps) without seeing any map, and a third agent aligned each map to it. All prompts, outputs and scripts are in `process-mapper/research/data/`.

## 2. Results

### 2.1 Reading is not the problem

PET benchmark, 44 documents, one example in the prompt, three models: activity F1 0.92 to 0.93, actor F1 0.91 to 0.92, direct-successor F1 0.74 to 0.76, ordered-pair F1 0.70 to 0.75. Reversed order: 0.2 to 0.6 per cent of pairs. Published systems score 0.69 to 0.74 on mentions and 0.72 to 0.89 on relations (different metric definitions; the comparison supports only "at or above"). Long descriptions cost order, not steps: successor F1 falls from 0.81 to 0.70 past eight sentences. Model size changes little (the three models agree on 88 to 90 per cent of activities).

### 2.2 Finland: the public map against the agency's own guidelines

84 steps, two judges, both rounds (benefit guideline, then the three cross-benefit guidelines for the 24 appeal, recovery and correction steps).

| Verdict | Opus judge | Sonnet judge | Both agree |
|---|---|---|---|
| Described as a step | 16 | 16 | 45 (step, or step with a detail wrong) |
| Step exists, detail differs | 38 | 33 | |
| Only the rule is stated | 24 | 29 | 21 |
| Not mentioned | 5 | 5 | 5 |
| Contradicted | 1 | 1 | mixed: 13 |

The five absent steps: the online calculator, two State-funding transfers, and two steps from an internal note on a termination robot that the guideline does not cover. The one contradiction: the map had a caseworker decide whether a decision is appealable before an appeal is filed; Kela has no power to refuse an appeal ("Kelalla ei ole toimivaltaa jättää valitusta tutkimatta"); the system prints the appeal bar and any appeal is forwarded to the Board. A rule became a gate.

What "detail differs" means, in four families:

- **Actor and automation (largest).** 29 steps assigned to the Kela system: 5 confirmed automatic (annual-review letter, programmatic termination when the review is not returned, Incomes Register and lease-data feeds), 5 given to a caseworker (requesting missing information "primarily by phone", reading background data, valuing assets, judging accepted costs, the inputs to the calculation), 19 silent. The guideline uses "ohjelmallisesti" twice in 83 pages.
- **Stale law.** The Finlex consolidation stops in 2017. The map carried the 80 per cent rate, the EUR 300 earned-income deduction (ended 31 March 2024) and owner-occupied dwellings (excluded from 2025). The guidance in the corpus had the current values; the synthesis logged the conflict as a question instead of resolving it.
- **Order and triggers.** Both judges contradict 3 steps: a non-returned annual review is terminated by the program, not routed to a caseworker; an overpayment arises inside a revision or termination decision, not as a separate event; termination dates follow a table of grounds. Several branches (change report, landlord notice, appeal) were started as separate flows that loop back, so the reference's "after the decision" reads as "before" in the map.
- **Granularity.** 12 steps the guideline splits (correction into five procedures), 7 to 10 it merges (completeness check and eligibility check fold into "map the household's overall situation first").

**Two sources beat one.** Steps supported by facts from two or more public documents: confirmed as a step by both judges 25 of 52 (0.48), absent 6 of 52 (0.12). Single-source steps: 4 of 32 (0.13) and 11 of 32 (0.34). The single-pass Opus map shows the same: 2 of 66 multi-source steps absent, 9 of 24 single-source.

**The confidence score does not predict confirmation.** Two-pass map: steps rated 0.7 to 0.89 were confirmed as steps 31 per cent of the time, steps rated below 0.7 65 per cent. The rubric scores how explicit the source is, not whether the agency recognises the step. The Opus single-pass score was better behaved (59 per cent at 0.9 and above, 2 per cent absent) but still not a probability.

**Recall.** The guideline-only reference has 129 steps (83 caseworker, 15 citizen, 5 automatic, 20 unclear, 3 landlord, 3 other authority). The two-pass map matches 52 of them (40 per cent): appeals 5 of 5, termination 5 of 7, payment 6 of 14, data gathering 7 of 27, decision 2 of 8, intake 3 of 9. What it misses is case-specific caseworker work: cohabitation checks, re-letting consent, imputed minimum income, asset valuation sources, Åland routing, landlord recovery.

**What even the staff guideline does not say.** It refers 42 times to a separate process description ("yleisen asumistuen prosessi"), 23 times to situation-specific action instructions, 13 times to case-system registration instructions, all intranet-only. Of the map's 16 open questions, the guideline answers 4, half-answers 10, and 14 of 16 point onward to another internal document. The rules layer is public in Finland; the process layer is not, even for the agency's own published guideline.

### 2.3 Pipelines and inputs

Same corpus, different builds, all aligned to the 129-step reference by the same kind of judge (Opus). "Order" counts consecutive reference pairs where the generated map has the same order.

| Build | Steps | Reference steps recovered | Generated steps matched | Order right / checked |
|---|---|---|---|---|
| Two-pass, facts then synthesis (existing pipeline) | 84 | 52 (40%) | 56 (67%) | 33 / 46 |
| Single pass, Sonnet, run 1 | 100 | 63 (49%) | 77 (77%) | 57 / 60 |
| Single pass, Sonnet, run 2 | 110 | 65 (50%) | 86 (78%) | 53 / 60 |
| Single pass, Sonnet, run 3 | 95 | 75 (58%) | 75 (79%) | 53 / 60 |
| Single pass, Haiku | 77 | 48 (37%) | 58 (75%) | 32 / 45 |
| Single pass, Opus | 90 | 68 (53%) | 64 (71%) | 49 / 60 |
| Single pass, Sonnet, public documents plus the internal note | 107 | 67 (52%) | 76 (71%) | 49 / 60 |
| Law only | 113 | 54 (42%) | 66 (58%) | 43 / 45 |
| Citizen guidance only | 83 | 53 (41%) | 66 (80%) | 45 / 49 |
| Application form only | 85 | 39 (30%) | 40 (47%) | 32 / 38 |
| Per document (no inference), then merge | 170 | 66 (51%) | 101 (59%) | 53 / 60 |
| Claims only: no inferred actor, no inferred order | 60 | 40 (31%) | 44 (73%) | 3 / 20 (15 unconnected) |

Readings.

- **Pipeline shape does not change the error profile.** Verified against the guideline, the single-pass Opus map (90 steps) gives 15 described, 25 with corrections, 39 rule-only, 11 absent, 0 contradicted; the two-pass map in the same round gave 11, 27, 29, 17, 0. Same families of correction, same stale rules, same "system" guesses (29 system steps, 2 confirmed).
- **Runs are not stable in size.** Three Sonnet runs on identical inputs: 95 to 110 steps, 44 to 52 of them "system". They recover largely the same reference steps (overlap 0.84 between runs 1 and 3), so the instability is in what gets padded, not in what gets found.
- **Order comes from the law and the guide.** Kendall's tau between the order of first mention in a document and process order: Act 0.64, benefit guide 0.68, service catalogue 0.70, citizen pages 0.36 to 0.42, form 0.11, parameter page 0.06. The law-only build gets 43 of 45 orders right; the form-only build 32 of 38 only because its loops make everything reachable.
- **The internal note adds its own branch and nothing else** (67 versus 63 to 75 recovered).
- **Decompose, then merge, gives the best recall per invented step.** 66 of 129 recovered; 43 of the 66 come from nodes that two or more documents support. But the merge is 170 nodes, 69 of them matching nothing in the guideline (form fields, rules as steps, events), so it is a candidate list for review, not a map.
- **Forbidding inference lowers recall and removes the invented structure.** The claims-only build names no actor for 35 of 60 steps because no public sentence names one, states 40 orders instead of 150 edges, and writes 24 questions. Checked against the benefit guideline (one Opus judge, same rubric), its 60 claims: 16 described as steps, 16 with corrections, 10 rule-only, 18 absent, 0 contradicted, and not one claim with a wrong actor. The absent ones are citizen channel steps (calculator, upload, postal address, status check), the State-funding transfers, and the appeal steps the guideline defers to the cross-benefit guideline. By share, 27 per cent of its claims are described as steps against 13 per cent for the two-pass map in the same round, and 27 per cent need a correction against 32 per cent. It recovers 40 reference steps and connects almost none of them. It is the honest map: everything in it is a sentence, and everything it does not know is a question.

### 2.4 Australia and Germany

**Australia.** Two public-page maps (Sonnet 60 steps, Opus 65) against the staff procedures: 9 and 6 described as steps, 25 and 24 with corrections, 9 and 14 rule-only, 16 and 21 absent, 1 and 0 contradicted. Of the absent, 6 and 13 are overseas-travel and indexation steps outside the eight procedure pages supplied. The corrections repeat Finland: staff decide eligibility and code the screens, the system only computes the rate; payment continues for 28 days while proof is awaited (the maps hold payment until proof is checked); if a customer ignores the request letter the whole main payment is suspended, not just Rent Assistance. Recall against the Blueprint's 192 non-screen steps: 53 of 135 work steps and 28 of 57 policy steps, mostly partial. Never mentioned in public: internal routing (16 steps), dates and arrears (15), special circumstances (15), handling returned proof (11), verification exemptions (9).

**Germany.** The law-only map (60 steps) against the government's own process model: 38 of 42 official activities matched (25 exact), with the same legal basis for 29 of 38. The 4 misses all rest on sections not supplied (security interview, federal identity assistance, fallback to another title). 24 of the 60 generated steps match nothing official: events, citizen-side steps, rules written as steps, and 12 steps the official model does not have (hardship commission, prosecutor's assessment, objection decision). Where the government models from the law, a map from the law reproduces it.

## 3. What this says about the approach

The two-pass design was right about one thing and wrong about another. Right: facts with verbatim quotes are checkable, and they checked (818 of 818 quotes verified; every variant here verified 100 per cent). Wrong: the synthesis step is asked to produce a complete BPMN-shaped graph, so it fills the fields the facts do not fill: actor, automation, trigger, the edge that closes the loop. Those fields are where the agency disagrees. The single-pass builds do the same thing. The problem is the output contract, not the number of passes.

Three facts from the data set the design.

1. Public documents state *rules* and the *citizen interface* well. They state *who does what inside* almost never (Finland: "ohjelmallisesti" twice in 83 pages of the staff guide; the public pages never). A pipeline that must output an actor for every step will guess, and the guess is wrong or unverifiable 24 times out of 29.
2. *Order* lives in two document types: the statute and the staff guide. Forms, parameter pages and catalogues carry none. A pipeline that reads them all with equal weight imports noise into the order.
3. The agency recognises a step when two public documents describe it (0.48 versus 0.13). Triangulation is cheap and it is the strongest single predictor found.

## 4. The pipeline to build now

Not a new architecture. A different contract, enforced by code.

1. **Claims, not graphs.** The unit is "actor A does X when T", each with one sentence. Fields the documents do not fill stay empty: `who: unknown`, `automation: unknown`, no edge. Empty is a result, not a failure.
2. **Order only from sources that carry it.** Edges come from the statute, the staff guide, and explicit words ("after", "then", "within 14 days of"). Everything else is a *question*, listed with the step it would attach to.
3. **Two sources per claim.** A claim with one source is marked single-source and goes to the review sheet first. The score is the count of independent documents, not a model's confidence.
4. **Rules stay rules.** Conditions and amounts are stored as rules linked to the step that applies them, never turned into decision nodes. This removes the one contradiction found in Finland.
5. **Point-in-time law.** Fetch the consolidation in force on the date of the map, and let a dated guidance page override a parameter in an older consolidation.
6. **Validation is the product.** The output is a review sheet: one line per claim, one sentence of evidence, four boxes (we do this; differently, how; we do not; ask X). Half a day of a process owner's time turns the map into the agency's statement. The questions list is the agenda.

Expected effect, from the data: recall of internal steps stays around 40 to 50 per cent from public documents (that is a ceiling of the documents, not the method), contradictions go to zero, wrong actors go to zero, and the number of claims a process owner must correct drops from about half to the share where triggers and granularity differ.

## 5. The live test

Run it with two or three Kela process owners, each independently, on the review sheet above, before any discussion. Measure acceptance per claim, recall against the steps they add, kappa between reviewers, and minutes per claim. Predictions committed now: recognition (box 1 or 2) above 0.85 for citizen-facing claims and 0.75 for internal ones; "we do not do this" below 0.05; reviewers add 15 to 40 steps, mostly data gathering and routing; two-source claims accepted at least twice as often as single-source; fewer than 5 per cent of order pairs reversed; under three minutes per claim. If "we do not do this" exceeds 0.05, the assumption fails in the way that matters.

## 6. Limits

- Judges are models, not Kela staff. Two judges agreed at kappa 0.70; the same judge family built the maps, so shared blind spots are possible. Every judge quote was checked against the reference text; verdicts were not.
- Alignment of maps to the reference is also a model's judgement; each alignment was one run. The size of the reference (129 steps) depends on how finely one agent split the guideline.
- "Not mentioned" in a staff guideline does not mean "not done". The Finnish guideline defers process to intranet documents; the Australian pages supplied do not cover travel or indexation.
- One service per country. Finland is a benefit with a published staff guide, Australia a benefit with screen-level procedures, Germany a permit with a government process model. Generalisation beyond means-tested benefits and permits is untested.
- The PET comparison uses different metric definitions from the published numbers.

## Files

`process-mapper/research/data/`: prompts (`prompts/`), scripts (`scripts/`), the Finnish verification outputs and reference (`fi/`), variant maps and alignments (`fi/variants/`), Australia (`au/`), Germany (`de/`), benchmark scores (`pet/`). Source corpora are re-fetchable from the URLs in each manifest; the Kela guidelines are at `kela.fi/etti/<name>.pdf`.
