# Can a map become a parallel system? First run of the twin

November 2026. One service, the general housing allowance (Kela, Finland). One question: when the
process map is loaded as the specification of a second implementation, does that implementation
decide cases the way the real system does, and where it does not, does the divergence tell us
something about the map?

Code: `process-mapper/twin/`. Everything below is reproducible from `python -m twin.cli`.

## The answer so far

1. **The rules layer of the map is executable and correct where it can be checked.** The twin
   reproduces all 36 income limits Kela publishes (three municipality tables, one to three adults,
   zero to four children) from the formula, with no fitted parameter. Kela's three worked examples
   (Turku couple 125.65 EUR, Helsinki cap 563 EUR, asset conversion 83.33 EUR per month) pass as tests.
   Against Kela's online calculator (laskurit.kela.fi, 1 November 2026 parameters), 28 of 28
   runs agree to the cent: 23 grid households across the three mainland tables, one to three adults,
   zero to three children, incomes from 0 to 2,600 EUR, plus separate water, separate heating in
   Lapland, 25,000 EUR of deposits, and five variants with electricity included in the rent. The
   twin's inputs and the calculator's results are in `twin/oracle/`, with screenshots.
2. **The whole application path runs.** 410 synthetic households walk 24 steps of the map from
   application to the payability decision. Per run: 7 steps by rules, 6 by the judge, 4 by register
   adapters, 5 taken from the application, 1 drafted notice, 1 gate where the run stops with a
   proposal for a person. Outcomes: 323 granted, 82 below the 15 EUR minimum, 4 rejected on an
   eligibility ground (assets, student, pension, owner-occupied), 1 question (rent not stated).
3. **Published appeal decisions replay, and they correct the twin.** 12 decisions of the Social
   Security Appeal Board (9) and the Insurance Court (3), 2017 to 2025, each turned into a case
   with verbatim quotes. On the facts as the appeal body stated them, the twin reaches the body's
   eligibility outcome in 9, asks a question instead of deciding in 1 (a minor applying alone),
   cannot test 1 (the rent is not stated and the dispute is about income), and differs on the amount
   in 1 by exactly the 2021 index adjustment the twin does not carry. Two rules were wrong in the
   first run and were corrected from the decisions: non-resident co-occupants leave the household
   and share the rent instead of disqualifying the applicant; a minor living apart from parents is a
   question, not a grant.
4. **Shadow mode exists and has not run on real cases.** The runner never acts; the shadow command
   reads a directory of mirrored cases and writes a divergence report. A two-phase demonstration in
   `twin/runs/shadow-demo/` shows the mechanics: week one, ten mirrored applications and no
   outcomes (report: ten cases awaiting the real decision); week two, outcomes added, nine agree
   and the one altered outcome is reported as an amount divergence of 12.00 EUR. What a partner agency must
   provide, and under what legal basis, is in `twin/SHADOW.md`. No agreement exists yet.

## What the calculator added to the map

Driving the calculator exposed three things the documents in the corpus do not state.

- When electricity is included in the rent, the calculator asks for the floor area and deducts
  0.86 EUR per square metre per month, the Tax Administration's in-kind value. No kela.fi page gives
  the figure; the staff guideline refers to the tax decision. The map's rule says only "electricity
  included in rent is deducted". The twin now carries the parameter, sourced to the calculator.
  In the five runs the rent stayed above the municipal cap after the deduction, so the parameter
  is recorded, not yet tested by a differing amount.
- The calculator expects the applicant to subtract the 2,000 EUR per-person deposit disregard
  before entering deposits; it does not apply it itself. The twin applies it. Entering 25,000 EUR
  raw in the calculator and 27,000 EUR gross in the twin gives the same 152.95 EUR. A shadow run
  that fed the calculator's input convention into the twin unchanged would show a divergence of
  33.33 EUR per month on every case with deposits, caused by the interface, not the rule.
- The published "income limits" already include the 15 EUR minimum payment, which is why the
  formula reproduces them only when the minimum is part of the inversion.

## What encoding the map found in the map

Turning rules into functions is itself a check. Each item below is a place where the map, built
from documents that predate 2025, differs from what kela.fi states today, or where the map left
something open that code cannot leave open.

| Finding | Map | kela.fi, October 2026 | Twin |
|---|---|---|---|
| Students | eligible household members; `R_ELIG_STUDENT` absent | "If you study, you cannot, as a rule, get general housing allowance" (moved to the study housing supplement) | new eligibility ground, dated parameter `students_excluded_by_default` |
| Compensation rate | 0.70 in guidance, 0.80 in the consolidated Act text; conflict logged | 0.70 mainland, 0.80 Åland | two dated sets; the Act-level set carries 0.80 |
| Earned income deduction | 300 EUR per member (`R_CALC_EARNED_INCOME_DEDUCTION`) | not mentioned | 0 in the current set, 300 in the Act-level set |
| Municipality groups | four Act groups | three tables (Espoo, Helsinki, Kauniainen and Vantaa together) plus Åland | group II resolved per parameter set |
| Owner-occupied homes | `R_CALC_LEGACY_OWNER_COSTS` with a warning | "not available for owner-occupied homes" | rejection ground now; owner-occupier cost formula not encoded for the older set (raises a question) |
| Basic deductible | current formula verified against two examples | 0.5 x [T - (667 + 94A + 296L)] | reproduces the 36 limits |
| `D_MIN_AMOUNT` | both outgoing edges lead to `T_DECIDE` | | the runner needs the state, not the edge, to know the decision; edge conditions are labels, not logic |
| `D_APPEALABLE` | caseworker decides appealability (contradicted in the validation study) | | not in the application path; left as mapped |
| Non-resident co-occupants | `R_ELIG_RESIDENCE` phrased as a membership condition; no cost-share rule for excluded occupants other than students | SAMU 2017: only the covered occupant is a member, one quarter of the rent accepted | household and cost share corrected from the decision |
| Minor applicant | `R_HH_ALWAYS_SAME` puts minor children with parents; nothing says what happens when a minor applies alone | SAMU 2020: remains in the parents' household unless own income suffices | twin asks instead of deciding |
| Electricity in rent | "electricity included in rent is deducted", no amount | calculator: 0.86 EUR per m2 per month | parameter added, sourced to the calculator |

Four of the first six are the map's stale-law problem from the validation study, now with a date on each
value. The fifth (students) is a legal change after the corpus was fetched. A map that is executed
finds its own staleness faster than a map that is read, and a map that is replayed against decided
cases finds the rules it does not have.

## What the twin is and is not

It is a twin of the decision function: application facts in, decision and amount out, every step
attributed to a rule, a register, a judge or a person. It is not a twin of Kela's internal routing:
the map's internal steps are walked in the map's order, and the trace records who the map says
does them, which the validation study showed is guessed for about half of the internal steps.

The judge is scripted: it answers judgment steps (residence, household, income, eligibility) from
the structured facts of the case. That is enough for synthetic, calculator and replay cases, whose
facts are already structured. A case that arrives as documents needs a model-backed judge with the
same signature, which is the next piece of code and the first one that needs a model key.

## Stage 3 detail

Cases: `twin/cases/replay/`, report: `twin/runs/replay/replay-report.md`. Sources and limits in
`twin/cases/replay/README.md`: the SAMU decision database holds 41 housing allowance decisions,
29 of them under the old Act and 3 on the pensioners' allowance; Finlex lists 5 Insurance Court
decisions since 2015, 2 of them pensioners'. The Ombudsman's site blocked automated access.

| Case | Dispute | Real outcome | Twin, first run | Twin, after correction |
|---|---|---|---|---|
| SAMU 2017 | three co-residents outside Finnish social security; one quarter of the rent accepted | revision upheld | rejected (residence rule applied to every occupant) | eligible; household of one; 828 x 1/4 = 207 EUR accepted |
| SAMU 2019 (3) | income averaging and revision threshold; summer job as continuous income; foster child | granted 30.96; revised; revised | eligible, amount unknown | same |
| SAMU 2020 | 15-year-old applying alone | rejected: part of parents' household | eligible (no rule) | question: independent household depends on own income |
| SAMU 2021 (3) | start date; entrepreneur at YEL income; alternating-residence child and extra space | granted; revised; granted 193.30 | eligible; eligible; 147.90 | same; the 45.40 EUR gap is the index |
| SAMU 2024 | share savings account gains as recurring income; deductible exceeded costs | terminated | eligible, amount unknown | untestable: rent not stated |
| VakO 2019 | correction to the applicant's detriment without consent | original 243.41 stands | eligible, amount unknown | same |
| VakO 2020 | group-home room under a lease is a rental dwelling | returned to Kela | eligible, amount unknown | same |
| VakO 2025 | five-year recovery limit per jointly liable member | recovery set aside | eligible, amount unknown | same |

The one amount divergence is informative. The decision states the 2021 maximum housing costs for
three persons in group IV (657 EUR) and the basic deductible (415.38 EUR on 2,143 EUR of counted
income). The twin's Act-level set gives 641 and 456.12. Inverting the deductible gives a
full-rate income threshold of 1,154 EUR for one adult and two children, against the Act's 1,057, which is the National Pension Index applied to the statutory constants. With the
2021 constants the formula gives 193.30 exactly. The rule is right; the parameter table needs a
row per year, which Kela's archived pages can supply.

What the decisions do not state limits what replay can test. Three of twelve state the rent, one
the municipality, none the ages, three an amount. Replay therefore tests the eligibility layer and
the legal characterisation of facts (is a group-home room a rental dwelling, is a foster child a
member, is a capital gain recurring income), not the arithmetic. The corrections it produced are of
that kind: both were about who is in the household.

## Stage 4: what a shadow run needs

- A partner. In this repository the nearest are the Romanian municipalities (Deta, Simeria), whose
  procedures are mapped and, for Simeria, verified against the office's own written procedure. The
  heating aid runner would be a second service on the same runner, which is the real test of the
  claim that the map structure is the same for every service.
- A mirror of the intake: the field list in `twin/SHADOW.md`, pseudonymised, no free text.
- The outcome feed: the agency's decision added to each case when it issues.
- A processor agreement (GDPR art. 28) and, advisably, a data protection impact assessment.
- A reading routine: a person on each side reads the weekly report; every divergence is classified
  as map error, parameter error, agency practice, or judge error before anything is changed.

## Limits

- The calculator and the published examples are Kela's own simplifications; they do not exercise
  income averaging, subtenants, split households, or the timing rules, which the twin encodes from
  the map but has not checked against any outcome.
- The Act-level parameter set carries statutory base amounts, not the index-adjusted values of each
  year, so amounts for pre-2024 replay cases are approximate; decisions are not. Kela's archived
  pages on the Wayback Machine would supply the yearly values, but the environment's egress policy
  blocks that host; this is the first thing to add.
- The map's internal steps (completeness check, information request, routing) are executed by the
  scripted judge and never reach a human in these runs. Nothing here measures how often a real
  caseworker would have asked for information.
