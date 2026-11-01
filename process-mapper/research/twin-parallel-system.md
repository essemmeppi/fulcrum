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
   CALCULATOR_RESULT
2. **The whole application path runs.** 410 synthetic households walk 24 steps of the map from
   application to the payability decision. Per run: 7 steps by rules, 6 by the judge, 4 by register
   adapters, 5 taken from the application, 1 drafted notice, 1 gate where the run stops with a
   proposal for a person. Outcomes: 323 granted, 82 below the 15 EUR minimum, 4 rejected on an
   eligibility ground (assets, student, pension, owner-occupied), 1 question (rent not stated).
3. REPLAY_RESULT
4. **Shadow mode exists and has not run on real cases.** The runner never acts; the shadow command
   reads a directory of mirrored cases and writes a divergence report. What a partner agency must
   provide, and under what legal basis, is in `twin/SHADOW.md`. No agreement exists yet.

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

Four of these are the map's stale-law problem from the validation study, now with a date on each
value. The fifth (students) is a legal change after the corpus was fetched. A map that is executed
finds its own staleness faster than a map that is read.

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

REPLAY_DETAIL

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
  year, so amounts for pre-2024 replay cases are approximate; decisions are not.
- The map's internal steps (completeness check, information request, routing) are executed by the
  scripted judge and never reach a human in these runs. Nothing here measures how often a real
  caseworker would have asked for information.
