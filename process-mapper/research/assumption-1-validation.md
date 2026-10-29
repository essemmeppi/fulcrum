# Can documents alone give a reliable map of a government process?

Validation study for assumption 1 of The Agentic State. Draft, October 2026.

## 1. The claim and what "reliable" means

The assumption: a reliable map of how a government entity runs a service can be built by reading its documents. Public documents (law, guidance, forms, catalogues) when that is all we have; internal documents (staff guidelines, process descriptions, system rules) when the entity collaborates.

"Reliable" has to be testable. We use three tests, from weak to strong.

1. **Extraction test.** Given one text that describes a process, does the pipeline find the steps and their order? This is the standard task in the process-extraction literature, with a gold-labelled benchmark. It shows the pipeline can read. It does not show the map is true.
2. **Internal-reference test.** Build the map from public documents only. Then compare it with what the entity tells its own staff to do. Every step gets one of five verdicts: described as a step, described only as a rule, described with corrections, contradicted, not mentioned. This is the test that matters for "yes, this is what we do", and it can be run without an interview wherever the staff guideline is published.
3. **Process-owner test.** A person who runs the process corrects the map step by step. We did not run this. Section 9 gives the protocol and the predictions we commit to before running it.

Two secondary properties also matter: **stability** (the same inputs give the same map twice) and **calibration** (the confidence score on a step predicts whether it is confirmed).

## 2. What is already known

- **Extraction from one text is a solved-enough problem.** On the PET benchmark (45 process descriptions annotated by Bellan, Dragoni and Ghidini, 2022), rule-based and CRF baselines reach F1 0.69 for mention detection and 0.72 for relation extraction. Neuberger and colleagues (2024) report GPT-4o at 0.74 and 0.89 with three examples in the prompt, and Claude 3 Opus at 0.73 and 0.91. Prompt design moves scores by 5 to 8 points; a bad prompt drops relation F1 to 0.56.
- **Two modellers do not draw the same model from the same text.** The PET authors note that one text admits several correct models. Witt and colleagues (2024) had legally trained coders encode the same statute: similarity between coders was 4% in week one and 58% after they agreed on key terms and validation rules. Reliability is a property of the method, not of the text.
- **Model quality has several dimensions.** Lauer and colleagues (2026) score BPMN models from language models and humans on 39 metrics: models win on syntax and layout, humans on semantics. Klievtsova and colleagues (2024) count 17 of 21 GPT-4 models as correct on a university test set, but assume the human models are correct.
- **Written process and practised process differ.** Lipsky's street-level bureaucracy, the "space in the rules" work on Ontario Works, and process-mining studies of de jure versus de facto models all find the same thing: documents say what should happen; staff do what the case needs. Wijnhoven and colleagues (2023) add that an incomplete documented model makes the gap hard to measure.
- **Comparing two process maps is its own problem.** Dijkman and colleagues (2011) compare label, structure and behaviour similarity; graph edit distance is NP-complete. Weidlich, Mendling and Weske (2011) propose behavioural profiles: for each pair of steps, strict order, reverse order, exclusive, or interleaving. We use the order relation between pairs of steps as the ordering metric throughout.

What is not known: whether a map built from public documents of a real public service matches the agency's internal procedure, and which inputs and pipeline choices move that match. That is what this study measures.

## 3. Data

| Set | Content | Role |
|---|---|---|
| PET v1.1 | 45 English process descriptions, 502 activities, 449 actors, 675 flow relations, gold-annotated | Extraction test |
| Kela public corpus | 7 public documents on Finland's general housing allowance: Act 938/2014 (Finlex consolidated text, stops at 2017 amendments), 4 citizen guidance pages and PDFs, application form AT 1e, Suomi.fi service record. 170,000 characters | Input to all map builds |
| Kela internal note | One published procedure note on automated termination when a pension is granted | Marginal-input test |
| Kela staff guideline | "Yleinen asumistuki" benefit guideline, 83 pages, dated 22 October 2026, "primarily for Kela's internal use", published as PDF on kela.fi | Internal reference |
| Kela common guidelines | Appeals (38 pages), recovery of overpayments (55 pages), correction and annulment of decisions (25 pages), same series | Internal reference for the appeal, recovery and correction steps |
| Services Australia public pages | 17 public Rent Assistance pages and 2 factsheets, 40,000 characters | Second jurisdiction input |
| Services Australia Operational Blueprint | 8 staff procedure pages for Rent Assistance with numbered step tables, 200,000 characters | Second jurisdiction reference |

The German FIM portal publishes official process models in XProzess format (we downloaded one, for humanitarian residence permits: 42 activity groups with legal bases). No Wohngeld (housing benefit) process is in the catalogue, so we did not use it.

## 4. Methods

All model calls ran as Claude agents (Haiku 5.5, Sonnet 5.5, Opus 5.5) with fixed prompts stored next to the data. No model saw the reference documents while building a map. No judge saw another judge's verdicts. Quotes in every output were checked by code against the source text after whitespace and punctuation normalisation; a quote that does not match is counted as unverified.

**E1, extraction test.** Each PET document is given with numbered sentences and tokens. The model returns activities (verb spans), actors (noun-phrase spans), performer links, and successor pairs (B directly after A). One annotated example document is in the prompt and excluded from scoring; 44 documents are scored. Metrics: precision, recall and F1 for activities and actors (strict span match and relaxed overlap match), performer pairs, successor pairs, and ordered pairs. Gold successor pairs are derived by collapsing gateways and conditions between activities. Ordered pairs use reachability: for every pair of gold activities the model found, is A before B in both graphs? Three models, same prompt.

**E2, internal-reference test.** The existing map (84 nodes, 95 edges, 79 rules, built by the two-pass pipeline from the 7 public documents plus the internal note) was checked node by node against the staff guideline by two independent judges (Opus and Sonnet) that read the whole guideline. Each verdict carries verbatim quotes with page numbers. The 24 appeal, recovery and correction nodes were then checked in a second round against the three common guidelines. We report verdict shares, judge agreement (Cohen's kappa), actor and automation disagreements, order contradictions, calibration of the pipeline's confidence score, and the effect of multi-source support. A separate agent built a reference step list from the guideline alone, without seeing the map; a third agent aligned the two.

**E3, pipeline variants and inputs.** Same corpus, different builds: direct single-pass map (three models, three repeats for Sonnet), public documents only versus public plus the internal note, law only, guidance only, form only, and per-document maps merged afterwards. Each build is scored on structure (nodes, edges, dangling edges), evidence (share of quotes that verify), and recall of the guideline-derived reference steps after alignment. Stability is the share of nodes matched between repeats.

**E4, ordering information in documents.** For the reference steps, the position of their first mention in each public document is compared with their process order (Kendall's tau). This measures how much order information each document type carries before any model reads it.

**E5, second jurisdiction.** Maps built from the Services Australia public pages (Sonnet and Opus) are verified against the Operational Blueprint by one judge. The Blueprint is written at screen and field level, so this test also measures the granularity ceiling of public documents.

## 5. Results: extraction test (E1)

44 PET documents, one worked example in the prompt, three models, same prompt. Spans are scored strict (exact tokens) and relaxed (overlap). "Ordered pairs" are pairs of gold activities the model found, with A before B in the gold flow graph; the model is right if it also puts A before B.

| Metric | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 | Published reference |
|---|---|---|---|---|
| Activity F1, strict span | 0.90 | 0.88 | 0.90 | 0.69 (CRF, 7 types); 0.74 (GPT-4o, 7 types) |
| Activity F1, relaxed | 0.92 | 0.92 | 0.93 | |
| Actor F1, relaxed | 0.92 | 0.91 | 0.92 | |
| Performer link F1 | 0.77 | 0.75 | 0.77 | |
| Direct successor F1 | 0.74 | 0.74 | 0.76 | 0.72 (ML baseline, all 6 relations); 0.89 (GPT-4o) |
| Ordered-pair F1 | 0.70 | 0.73 | 0.75 | |
| Ordered pairs reversed | 0.6% | 0.5% | 0.2% | |

The published numbers are not directly comparable: they score seven entity types and six relation types, and the relation scores in Neuberger and colleagues (2024) are computed with gold mentions supplied. Ours score activities and actors only, and the successor score is end to end (the model's own activities, collapsed over gateways). The comparison supports one claim only: current models read a process description at or above the level of the specialised systems in the literature, with one example and no training data.

Three things matter more than the headline numbers.

1. **Direction is almost never wrong.** When the model orders two steps, it reverses the true order in 0.2 to 0.6 per cent of pairs. The 25 to 30 per cent of ordering errors are missing links and extra links (a skipped optional step, a loop the text implies but does not state, a parallel branch read as a sequence), not steps in the wrong order.
2. **Length hurts order, not step detection.** On the 29 documents of eight sentences or fewer, successor F1 is 0.80 to 0.82; on the 15 longer ones it is 0.68 to 0.72. Activity F1 drops by only 0.04. The reading is fine; keeping a long control flow straight is the weak point. A government process is a long document.
3. **Model size matters little here.** The three models agree on 88 to 90 per cent of activities (Jaccard), and the cheapest is within 0.03 F1 of the largest on every metric. The remaining errors are annotation conventions (whether "waits" or "goes to" is a step; whether a verb in an "if" clause counts), on which the gold is itself inconsistent in places (doc-1.1 has a branch with no incoming flow). These are ambiguities of the task, not of the models.

Conclusion for the assumption: extraction from one text is not the risk. Everything that follows is about multi-document reconstruction, where there is no gold and the authority is the only judge.

## 6. Results: internal-reference test (E2)

### 6.1 Verdicts on the 84 public-document steps

Two judges read the full 83-page staff guideline and gave each node one verdict. All 357 quotes the judges cited were checked by code against the guideline text; all 357 match verbatim.

| Verdict | Opus judge | Sonnet judge |
|---|---|---|
| Described as a step (who does what) | 11 | 10 |
| Step exists, material detail differs | 27 | 25 |
| Only the rule or amount is stated, not the step | 29 | 31 |
| Not mentioned | 17 | 18 |
| Contradicted | 0 | 0 |

Judge agreement: Cohen's kappa 0.67 on the five-way verdict, 0.70 when "described" and "differs" are pooled (raw agreement 0.81). The 16 disagreements are all between "the step exists" and "only the rule is stated"; no node is "exists" for one judge and "absent" for the other, except one (T_FORWARD_APPEAL).

Where both judges agree (68 of 84 nodes):

| Both judges say | Nodes | Of the 32 citizen-facing | Of the 52 internal |
|---|---|---|---|
| Step exists in the guideline | 29 | 11 | 18 |
| Only the rule is stated | 22 | 7 | 15 |
| Not mentioned | 17 | 9 | 8 |

Reading of the table. **No step is contradicted.** The public documents did not produce a false process. **Most steps exist**: 56 of 84 are confirmed as a step by at least one judge, and 22 more are confirmed as a rule the authority applies. **But only 11 to 15 of 84 are described in the guideline as a step with an actor doing it.** The staff guideline is a rules document, not a process document: it refers 42 times to a separate "yleisen asumistuen prosessi" (process description) that lives on the intranet, and 23 times to situation-specific action instructions. The process layer is where the map's remaining uncertainty sits, and it is not public even in a country that publishes its staff guidelines.

The 17 "not mentioned" nodes fall in three groups: 12 appeal and recovery-end steps that Kela documents in three cross-benefit guidelines (checked separately in 6.4); 3 steps from the internal note on automated termination (impulse task, robot outcome, state funding), which the benefit guideline does not cover; and 2 the public record overstated (the online calculator as a step; the State funding transfer as a step in the citizen's process).

### 6.2 What the map got wrong

The corrections cluster in four kinds. Each is a kind of error that document-based mapping will produce again, so each needs a mitigation.

1. **Actor and automation.** The map assigned 29 nodes to the Kela system or robot. The guideline confirms automation for 5 of them (annual-review letter, programmatic termination on a non-returned review, Incomes Register and lease-data feeds) and gives 5 to a caseworker instead: requesting missing information (done "primarily by phone"), reading background and population-register data, valuing assets, judging accepted housing costs, and the inputs to the calculation. For 19 the guideline is silent. The public record describes the data feeds and lets the reader infer automation; the guideline shows judgment sits in front of every computation. **Mitigation: treat "system" as unproven unless a document says "ohjelmallisesti" or names a robot; the map's agent-mode labels for internal steps must default to "agent prepares, human decides".**
2. **Stale law.** The Finlex consolidated Act stops at the 2017 amendments. The map carried the 80 per cent rate, the 2010-era deductible parameters, the EUR 300 earned-income deduction (in force only to 31 March 2024) and owner-occupied dwellings (excluded from 1 January 2025), each flagged by a judge. The citizen guidance in the corpus had the current values, and the map's synthesis recorded the conflict as an open question rather than resolving it. **Mitigation: fetch the point-in-time consolidation, and let guidance override the Act on parameters when the Act's consolidation date is older than the guidance.**
3. **Order and triggers.** Both judges contradict the order at 3 nodes: a non-returned annual review is terminated by the program, not routed to a caseworker; an overpayment arises inside a revision or termination decision, not as a separate system event; termination dates follow a table of grounds rather than one caseworker step. One judge also corrects the "no change" end state: under the protective rule a decision is still issued and payment continues. **Mitigation: these are exactly the places where a process owner's five minutes are worth more than any further document.**
4. **Granularity.** The judges mark 12 nodes that the guideline splits (decision correction into five procedures; termination into reason-specific rules) and 7 to 10 it merges (completeness check and eligibility check fold into "map the household's overall situation first"). The public record has the right steps at the wrong grain about one time in five.

### 6.3 Calibration and triangulation

The pipeline gave each node a confidence score by rubric. Does the score predict confirmation?

| Pipeline confidence | Nodes | Confirmed as step (Opus) | Confirmed as step or rule (Opus) |
|---|---|---|---|
| below 0.70 | 17 | 0.65 | 1.00 |
| 0.70 to 0.89 | 45 | 0.31 | 0.67 |
| 0.90 and above | 22 | 0.59 | 0.91 |

The score is not monotone. The low band is small and consists of internal steps the pipeline rated as implied; they turn out to exist. The middle band holds the appeal chain and the State-funding steps, which the benefit guideline does not cover. The rubric scores "how explicit is the source", which is not the same as "how likely is the agency to recognise this step". A calibrated score needs a reference, and this study produces the first one.

Multi-source support predicts confirmation better than the score:

| Support in the public corpus | Nodes | Both judges: exists | Both judges: absent |
|---|---|---|---|
| Facts from one source | 32 | 4 (0.13) | 11 (0.34) |
| Facts from two or more sources | 52 | 25 (0.48) | 6 (0.12) |

A step that two independent public documents describe is four times as likely to be confirmed as a step, and three times less likely to be absent. **This is the operational answer to "reading text does not prove the steps are right": require two documents per step, and treat single-source steps as questions for the process owner.**

### 6.4 The appeal, recovery and correction steps against the cross-benefit guidelines

The 24 nodes that the benefit guideline left unmentioned or rule-only were checked against the three cross-benefit guidelines (appeals, recovery, correction and annulment; 118 pages together).

| Verdict (Opus judge) | Nodes |
|---|---|
| Described as a step | 5 |
| Step exists, material detail differs | 15 |
| Only the rule is stated | 3 |
| Contradicted | 1 |
| Not mentioned | 0 |

[fill sonnet round 2 + agreement]

With the right internal document, nothing is absent. The one contradiction is instructive: the public map had a caseworker decide whether a decision is appealable before the appeal is filed, with an end state "not appealable". The appeals guideline says Kela has no power to refuse an appeal ("Kelalla ei ole toimivaltaa jättää valitusta tutkimatta"); the system prints the appeal bar on the decision, and any appeal filed is processed and forwarded to the Board, which alone may dismiss it. The public documents state the rule (some decisions cannot be appealed) and the map turned a rule into a gate. The 15 corrections are of the same family as in 6.2: collection runs largely by program and only after both decisions are final; a correction against the client needs written consent or an annulment by the Board; a further appeal to the Insurance Court goes back through Kela for self-correction and a statement; recovery decisions above EUR 5,000 need a service-unit director. The actor differs for 9 of the 24 nodes.

Combined over both rounds, the public-document map's 84 nodes end as: 0 absent from the internal record, 1 contradicted, about 70 confirmed as steps (half of them with a correction), and the rest confirmed as rules. The agency's own documents recognise the map; they also correct about every second internal step in some detail.

### 6.5 Recall: what the guideline describes that the public map lacks

[fill alignment]

### 6.6 The 16 open questions

Of the 16 questions the public-document map left open, the guideline answers 4 fully, 10 partly, and 2 not at all; 14 of the 16 point onward to another internal document. Fully answered: the current parameters (70 per cent, the 2024 deductible, the asset test), the Åland regime, the household test in unclear cases, and the trigger for paying the landlord directly. Not answered: the appeal channels and periods, and the combined general-support application. The pattern is the same as for the nodes: the staff guideline settles rules, and defers process.

## 7. Results: pipeline variants and inputs (E3, E4)

### 7.1 How much order is in the documents before any model reads them (E4)

For each public document, the map's nodes were ordered by where their earliest quote sits in that document, and that order was compared with the nodes' depth in the process (Kendall's tau; 1.0 means the document mentions steps in process order, 0 means no relation).

| Document | Nodes it supports | Tau, all nodes | Tau, main flow only |
|---|---|---|---|
| Act 938/2014 | 70 | 0.64 | 0.50 |
| Benefit guide (PDF, English) | 20 | 0.68 | 0.61 |
| Suomi.fi service record | 7 | 0.70 | 0.70 |
| Citizen page (English) | 33 | 0.42 | 0.51 |
| Citizen page (Finnish) | 33 | 0.36 | 0.42 |
| Internal note on automated termination | 14 | 0.72 | 0.20 |
| Application form AT 1e | 15 | 0.11 | 0.11 |
| Income and costs page | 11 | 0.06 | 0.06 |

The Act is written in process order (apply, assess, decide, pay, review, recover, appeal) and carries most of the order information; so does the benefit guide. The form and the parameter page carry none: they are organised by topic. This is why a law-only build gets the skeleton right and a form-only build does not, and why the order of a step should be sourced from the Act or the guide and never from a form. It also says that about a third of the ordering signal in the full map does not come from any document's text order: it comes from the model's reading of conditions and triggers across documents, which is exactly where the three order contradictions in 6.2 sit.

### 7.2 Pipeline and input variants (E3)

[fill E3]

## 8. Results: second jurisdiction (E5)

[fill]

## 9. Protocol for the process-owner test, and predictions

The internal-reference test is the strongest test that can be run without the agency. The process-owner test is the one that settles the assumption, and it should be run as an experiment, not a workshop.

**Participants.** Two to three people who run the process at Kela (a benefit specialist who maintains the guideline, a team lead from a processing unit, one caseworker). Each reviews independently before any discussion.

**Instrument.** The map as a list of steps in process order, each with name, actor, what it consumes and produces, the rule it applies, and the sentence of the public record it rests on. For each step the reviewer ticks one box: *this is what we do*; *we do this but differently* (and writes the difference in one line: actor, trigger, order, split or merge); *we do not do this*; *I do not know, ask X*. At the end of each sub-process: *what is missing here?* The reviewer never sees the pipeline's confidence score, so the score can be tested against the ticks.

**Measures.** Acceptance rate (box 1) and recognition rate (boxes 1 and 2) per step, overall and by visibility, by automation class, and by number of supporting sources; inter-reviewer agreement (kappa); recall against the steps reviewers add; calibration of the confidence score against the ticks; and the time a reviewer needs per step. A separate ordering sheet lists 40 pairs of steps and asks "which comes first, or neither"; the map's order is right or wrong per pair.

**Predictions we commit to before running it**, from the numbers above.

1. Recognition rate (boxes 1 and 2) above 0.85 for citizen-facing steps and above 0.75 for internal steps; acceptance without correction (box 1) between 0.45 and 0.60 overall.
2. "We do not do this" below 0.05 of steps; the cases will be rules the map turned into gates, as in 6.4.
3. Reviewers will add 15 to 40 steps, mostly data gathering, case-system registration and situation-specific handling, as in the guideline-derived reference (6.5).
4. Steps with two or more public sources will be accepted at least twice as often as single-source steps.
5. Ordering: fewer than 5 per cent of pairs reversed; 15 to 25 per cent "neither, they are parallel" where the map has a sequence.
6. The pipeline's confidence score will not predict acceptance (rank correlation below 0.2) unless re-based on the measures in 6.3.
7. A reviewer needs under three minutes per step; a full review of an 84-step map fits in half a day.

If predictions 1, 2 and 5 hold, the assumption holds in the form that matters: the agency recognises its process in a map built from its documents, and corrects it at the margin. If prediction 2 fails, the assumption fails: a map that invents steps the agency does not perform is worse than no map, because it looks authoritative.

## 10. What this means for the assumption

[fill]

## 11. Limitations

[fill]

## Files

[fill]
