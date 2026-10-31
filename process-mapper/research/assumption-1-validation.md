# Can documents give a process map the agency will sign?

Validation of assumption 1. October 2026. Four countries, four kinds of reference, one question: when a model reads an agency's documents and draws the process, does the agency's own record say "yes, this is what we do"?

## The answer in six lines

1. **Steps: yes, with corrections.** Finland, 84-step map from public documents, checked step by step against Kela's internal staff guidelines by two independent judges: 0 to 1 step contradicted, 5 absent, 45 confirmed as steps, 21 confirmed as rules. Australia and Germany give the same picture.
2. **Order: direction is right, links are missing.** Reversed order is rare (under 1 per cent of pairs on the benchmark, 3 of 84 steps in Finland). The errors are missing and extra links, and triggers that start a branch at the wrong point.
3. **Actors and automation: not from public documents.** The maps call 30 to 50 per cent of steps "system". The staff guideline confirms 5 of 29, gives 5 to a caseworker, and is silent on 19. This is where "synthesis without reality" shows: the model fills a field the documents never answer.
4. **Coverage: half.** Public documents recover 40 to 58 per cent of the steps the staff guideline describes. What they miss is uniform across countries: case-by-case data gathering, internal routing, exception handling.
5. **The lever is not the pipeline shape.** Two-pass and single-pass, three models, give the same error profile. What moves the result: which documents are read (the law and the staff guide carry the order; forms carry none), whether a step has two independent sources (four times the confirmation rate), and whether the pipeline is allowed to invent actors and order.
6. **Reading everything, one source at a time, works.** Romania, 13 public documents read in rank order into a ledger of claims with a change log: 82 claims, checked against a town hall's internal procedure the builder never saw: 0 contradicted, 28 of the 35 in-scope claims recognised, 35 of the procedure's 50 steps recovered, 0 order pairs reversed. Reading the same documents in reverse order gives the same process (76 of 82 claims match, 0 reversed) cut more coarsely. Every actor error is the same error: the law says "the mayor", the desk says "staff".

## 1. What was tested

| Country, service | Built from | Checked against | Why this reference |
|---|---|---|---|
| Finland, general housing allowance (Kela) | 7 public documents: Act, 4 guidance pages and PDFs, form, service catalogue (170k chars) | Kela's staff benefit guideline (83 pages, "primarily for internal use", published as PDF) plus 3 cross-benefit staff guidelines (appeals, recovery, correction; 118 pages) | What the agency tells its own staff |
| Australia, Rent Assistance (Services Australia) | 19 public pages and factsheets (40k chars) | Operational Blueprint: 8 staff procedure pages with numbered step tables (200k chars) | Screen-level staff procedure |
| Germany, residence permit on humanitarian grounds | Statute text only: 17 sections of the Residence Act, 7 of the Administrative Procedure Act (78k chars) | The federal FIM reference process model (42 activity groups with legal bases, government-authored) | The government's own process model |
| Romania, heating aid and energy supplement (Law 226/2021), town-hall level | 13 public documents read one at a time in rank order: norms, law, seven town-hall notices, the national catalogue entry, three press explainers (590k chars) | The operational procedure of the Simeria social-assistance directorate (33 pages with flowcharts, one of 53 it publishes under the internal-control standard) | A local office's own written procedure |

Plus the standard academic benchmark (PET, 45 annotated process descriptions) to show the reading step itself works.

**Method, in one paragraph.** Maps were built by Claude agents (Haiku, Sonnet, Opus 5.5) from the public documents only; no builder saw a reference. Each step of a map was then given one of five verdicts by a judge that read the whole reference: *described as a step* (who does what), *step exists but a detail differs* (actor, automation, trigger, order, granularity), *only the rule is stated*, *contradicted*, *not mentioned*. Every quote a judge cited was checked by code against the reference text (357 of 357 verbatim in the Finnish round). Two judges (Opus, Sonnet) rated the Finnish map independently: kappa 0.70. Recall was measured the other way round: an agent wrote the process from the staff guideline alone (129 steps) without seeing any map, and a third agent aligned each map to it. Romania used a different build (section 2.5): sources read one at a time, a ledger of claims updated after each, and the same verification afterwards. All prompts, outputs and scripts are in `process-mapper/research/data/`.

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

### 2.5 Romania: every source, one at a time, in rank order

The service is run by town-hall social-assistance directorates (DAS) and paid through county agencies (AJPIS). The builder read 13 public documents in rank order: [1] the methodological norms HG 1073/2021 with their annex forms, [2] the law, [3] seven town-hall notices and guides (Galați, Suceava, Târgu Mureș, Sânnicolau Mare, Șimleu Silvaniei, Scobinți, Bucovăț), [5] the national service catalogue entry, [6] three press explainers. After each source it updated a ledger of claims ("actor A does X when T", one sentence each, `who: unknown` allowed, rules kept apart, order only where the text states it) and appended a change log. Contradictions stay visible under a precedence rule: the later-dated source wins on amounts and dates and both values are kept; the norms and the law win on structure; silence never loses to inference. Held out: the Simeria procedure, from which 50 reference steps were written (22 DAS staff, 12 mayor, 6 citizen).

**Learning curve, forward run.**

| Source read | Claims added | Confirmed | Refined | Contradictions |
|---|---|---|---|---|
| 1. Norms HG 1073/2021 | 56 | 0 | 0 | 0 |
| 2. Law 226/2021 | 18 | 16 | 18 | 4 |
| 3. Seven town-hall notices, total | 7 | 33 | 8 | 10 |
| 5. National catalogue entry | 1 | 3 | 0 | 2 |
| 6. Three press explainers | 0 | 9 | 0 | 2 |

- After the norms and the law the ledger holds 74 of its final 82 claims. The notices add intake windows, the fiscal certificate and the rejection of incomplete files, and supply 10 of the 18 contradictions, 8 of them dates and amounts that differ by year or town. The catalogue adds one claim and two structural contradictions: "Complet online" where the norms allow electronic filing only where the town hall has built an intake system, and "decision" where the law says a mayor's disposition. The press adds nothing: two of the three articles reprint the law, and the ledger refused to count a reprint as independent confirmation.
- **Reverse order gives the same process and different bookkeeping.** Press first, norms last: the reprint added 30 claims up front and the norms then confirmed 46. Aligned claim by claim, 76 of the 82 forward claims have a counterpart, 0 of 32 shared order pairs are reversed, actors agree on 31 of 35 exact pairs. The reverse ledger is coarser (62 claims, 39 merges), cites more sources per claim and logs a different contradiction list (7 shared, 8 forward-only, 4 reverse-only). Order changes how finely the process is cut and which disagreements get noticed, not what the process is.
- Two runs in the same order: 82 and 68 claims, recovering 35 and 36 of the 50 reference steps. Size unstable, content stable, as in Finland.

**Against the Simeria procedure.** One Opus judge, the five verdicts of section 1, 170 quotes checked against the procedure text.

| Verdict | All 82 claims | 35 inside the town hall (citizen, DAS, mayor) | 47 outside (suppliers, AJPIS, ministry, owners' associations) |
|---|---|---|---|
| Described as a step | 16 | 11 | 5 |
| Step exists, detail differs | 25 | 17 | 8 |
| Only the rule is stated | 2 | 0 | 2 |
| Not mentioned | 39 | 7 | 32 |
| Contradicted | 0 | 0 | 0 |

Inside the town hall, 28 of 35 claims are recognised. Outside, the procedure is silent by scope: it covers gas, electricity and solid fuel and excludes district heating, so the owners'-association chain and the AJPIS-to-ministry budget chain never appear. The seven in-scope misses are the prefect, data-exchange protocols, electronic take-over of documents and mayor-level steps the law describes and the procedure gives to nobody.

"Detail differs" here is one family. **The law says "the mayor"; the procedure says staff.** All 7 actor disagreements go the same way: in the law the mayor requests documents, orders the home inquiry, draws up the monthly statements and the statistical reports; in Simeria DAS staff do each and the mayor signs. The law is written at the level of the legal person, the procedure at the level of the desk. Granularity: 14 claims the procedure splits (one disposition is drafted by DAS, endorsed for legality by the Secretary General, registered by the legal office, signed by the mayor), 2 it merges. Order: 24 supported, 58 silent, 0 contradicted. Two-source claims recognised 33 of 51 (0.65), single-source 10 of 31 (0.32): the Finnish ratio again.

**Recall.** 35 of 50 procedure steps recovered (22 exact), 0 of 29 checked order pairs reversed, 18 not connected because the ledger states order only where a document does. The 15 misses are the desk: endorsement of the application by the Taxes office and the Agricultural Register before filing, the completeness checklist, the register entry, the mayor's certification box, entry into the heating software, the amount calculation, the legality endorsement, the legal office, the director's signature, the borderou, the settlement list, the payroll. Read as rank 7, the procedure adds 11 claims, confirms 25, refines 10 and contradicts 4, two of them where its own flowcharts side with the norms against its text.

Finland, Australia and Romania give one answer: public documents contain the process the law describes, at the level of the legal person, with no contradictions and half the desk missing.

### 2.6 Where the documents are thin

Web probe, no code, for Guatemala (Mixco municipality, MIDES Bono Social), Indonesia (PKH, KTP-el) and South Africa (SASSA Child Support Grant). Mixco publishes a procedure manual of unusual quality (coded sheets, responsible positions, flowcharts, five editions since 2013) and nothing citizen-facing to check it against. South Africa has regulations that fix the counter steps and annual-report statistics, no staff procedure. Indonesia's PKH implementation guideline is cited in every thesis and retrievable from nowhere reachable here; district offices publish screen-level SOPs for KTP-el. Where a procedure manual is public the map comes from it directly and the test material is missing. Where it is not, the map is the law plus the catalogue, which is the "law only" row of section 2.3: 42 per cent recall, order right. Low information lowers recall of the desk; it did not produce a wrong map anywhere tested.

## 3. What this says about the approach

The two-pass design was right about one thing and wrong about another. Right: facts with verbatim quotes are checkable, and they checked (818 of 818 quotes verified; every variant here verified 100 per cent). Wrong: the synthesis step is asked to produce a complete BPMN-shaped graph, so it fills the fields the facts do not fill: actor, automation, trigger, the edge that closes the loop. Those fields are where the agency disagrees. The single-pass builds do the same thing. The problem is the output contract, not the number of passes.

Three facts from the data set the design.

1. Public documents state *rules* and the *citizen interface* well. They state *who does what inside* almost never (Finland: "ohjelmallisesti" twice in 83 pages of the staff guide; the public pages never). A pipeline that must output an actor for every step will guess, and the guess is wrong or unverifiable 24 times out of 29.
2. *Order* lives in two document types: the statute and the staff guide. Forms, parameter pages and catalogues carry none. A pipeline that reads them all with equal weight imports noise into the order.
3. The agency recognises a step when two public documents describe it (0.48 versus 0.13 in Finland, 0.65 versus 0.32 in Romania). Triangulation is cheap and it is the strongest single predictor found.
4. The order in which documents are read does not change the process found (Romania: 76 of 82 claims, 0 reversed pairs, in both orders). Reading the norms and the law first makes every later document a confirmation and a source of parameters; reading them last makes the early ledger coarse and the contradiction list different. Rank order is for bookkeeping and cost, not for correctness.

## 4. The pipeline to build now

Not a new architecture. A different contract, enforced by code, and a reading order.

1. **Claims, not graphs.** The unit is "actor A does X when T", each with one sentence. Fields the documents do not fill stay empty: `who: unknown`, `automation: unknown`, no edge. Empty is a result, not a failure.
2. **Order only from sources that carry it.** Edges come from the statute, the staff guide, and explicit words ("after", "then", "within 14 days of"). Everything else is a *question*, listed with the step it would attach to.
3. **Two sources per claim.** A claim with one source is marked single-source and goes to the review sheet first. The score is the count of independent documents, not a model's confidence.
4. **Rules stay rules.** Conditions and amounts are stored as rules linked to the step that applies them, never turned into decision nodes. This removes the one contradiction found in Finland.
5. **Point-in-time law.** Fetch the consolidation in force on the date of the map, and let a dated guidance page override a parameter in an older consolidation.
6. **Validation is the product.** The output is a review sheet: one line per claim, one sentence of evidence, four boxes (we do this; differently, how; we do not; ask X). Half a day of a process owner's time turns the map into the agency's statement. The questions list is the agenda.

Expected effect, from the data: recall of internal steps stays around 40 to 50 per cent from public documents (that is a ceiling of the documents, not the method), contradictions go to zero, wrong actors go to zero, and the number of claims a process owner must correct drops from about half to the share where triggers and granularity differ. Romania, built under this contract, hit each of these.

### 4.1 The run, step by step

Each step names the prompt or script that did it in this research, so the run can be repeated.

1. **Collect everything reachable.** Agency site, national catalogue, legislation portal, gazette, forms, ombudsman and audit reports, council minutes, freedom-of-information releases, press. Nothing is excluded. Record URL, date, publisher and type for each (`mapper/fetch.py`, a manifest per service).
2. **Rank by how procedural the document is**, not by legal authority: staff procedures and manuals, then implementing norms, then the statute, then agency guidance, then forms, then the catalogue, then press and minutes. Detect reprints: a document that copies another is a copy, not a source (the ledger found two of three press articles were the law). One short prompt over the first page of each document does the ranking; a human corrects it in minutes.
3. **Read rank 1 and write the ledger**: claims with one sentence each, unknowns left empty, rules apart, order only where stated, questions for every gap (`prompts/ro_sequential_ingestion.md`; the same contract as `prompts/fi_claims_map.md`).
4. **Read each next source and update**, appending to the change log what it added, confirmed, refined and contradicted, under the precedence rules above. Claims that only a low-ranked source supports carry a flag until confirmed (same prompt).
5. **Check by code**: every quote verbatim in its source, every claim with at least one quote, every order statement with a quote, no claim removed between two versions of the ledger without a change-log entry, source counts recomputed from the quotes (`scripts/check_variant.py`; the quote check is the one `mapper/extract.py` already runs).
6. **Write the review sheet**: one line per claim, the evidence, four boxes, single-source claims first, questions attached to the step they concern. Rules go on a separate sheet with their values by source and date.
7. **Counterpart review.** Half a day of a process owner. Their answers are the map's validation and the only one that counts (section 5).
8. **Re-run with the internal documents at the top of the ranking** once a collaboration gives them. The change log of that run is a deliverable in itself: what the public record does not say about this office (Simeria: 11 steps added, 10 actors refined, 4 contradictions, all inside the building).

The Romanian forward run was one agent reading 590k characters once, in order. Nothing in the run needs a graph until the agency has said yes.

## 5. Testing without holding anything out

Holding out the most procedural source was right for this research and wrong for production, where the map must use everything. With no hold-out the tests become these, all already run at least once above:

1. **Counterpart review** (below). The ground truth is the office, not a document.
2. **The change log as a saturation test.** When the last several sources add no claim and no contradiction, the public record is exhausted (Romania: ranks 5 and 6 added one claim). When a minor source adds structure, the ranking was wrong or the map is not done.
3. **Source count instead of leave-one-out.** A claim that disappears when one document is removed is a single-source claim. The count is already on every line; recognition of 0.13 to 0.32 for one source against 0.48 to 0.65 for two is the number to show the reviewer.
4. **Time split.** Build from documents dated before a point, check against documents after it. The 2021 norms and law predicted the 2023 to 2026 town-hall notices: 33 claims confirmed, 7 added, 10 contradictions of which 8 are dates and amounts.
5. **Jurisdiction split.** Build from one set of offices, check against another office's procedure. This is what Romania did: seven town halls in, Simeria out, 35 of 50, 0 contradicted. Any country with many local offices allows it for free.
6. **Two reading orders.** Claims that appear in one order and not the other are the unstable ones (6 of 82); order pairs that flip would be the unreliable ones (0 of 32).
7. **Traces.** Case files, decision registers, processing-time statistics, audit findings: the process as done rather than as written. Not tested here; it is what internal access buys.

**The live test.** Run it with two or three Kela process owners, each independently, on the review sheet above, before any discussion. Measure acceptance per claim, recall against the steps they add, kappa between reviewers, and minutes per claim. Predictions committed now: recognition (box 1 or 2) above 0.85 for citizen-facing claims and 0.75 for internal ones; "we do not do this" below 0.05; reviewers add 15 to 40 steps, mostly data gathering and routing; two-source claims accepted at least twice as often as single-source; fewer than 5 per cent of order pairs reversed; under three minutes per claim. If "we do not do this" exceeds 0.05, the assumption fails in the way that matters.

## 6. Limits

- Judges are models, not Kela staff. Two judges agreed at kappa 0.70; the same judge family built the maps, so shared blind spots are possible. Every judge quote was checked against the reference text; verdicts were not.
- Alignment of maps to the reference is also a model's judgement; each alignment was one run. The size of the reference (129 steps) depends on how finely one agent split the guideline.
- "Not mentioned" in a staff guideline does not mean "not done". The Finnish guideline defers process to intranet documents; the Australian pages supplied do not cover travel or indexation.
- One service per country. Finland is a benefit with a published staff guide, Australia a benefit with screen-level procedures, Germany a permit with a government process model, Romania a benefit with one small town's procedure. Generalisation beyond means-tested benefits and permits is untested.
- The Simeria procedure covers gas, electricity and solid fuel only, so 32 of the 39 "not mentioned" verdicts in Romania are out of scope rather than evidence either way. The town halls whose notices were read are not Simeria. The Romanian verification had one judge, not two.
- The PET comparison uses different metric definitions from the published numbers.

## Files

`process-mapper/research/data/`: prompts (`prompts/`), scripts (`scripts/`), the Finnish verification outputs and reference (`fi/`), variant maps and alignments (`fi/variants/`), Australia (`au/`), Germany (`de/`), Romania with its corpus, ledgers, change logs, reference and verifications (`ro/`, see `ro/manifest.md`), benchmark scores (`pet/`), the three-country document probe (`coverage/`). Source corpora are re-fetchable from the URLs in each manifest; the Kela guidelines are at `kela.fi/etti/<name>.pdf`.
