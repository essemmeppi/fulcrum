# Twin: a parallel system for a mapped public service

A second implementation of the general housing allowance (Kela, Act 938/2014), built from the
process map in `../maps/fi-kela-general-housing-allowance/map.json`. A case goes in as the law
defines it; a decision, an amount, a request for information or a notice comes out, with a trace
that cites the map's rules and, through them, the documents. The twin never acts on a citizen,
a register or a payment: in every mode it only produces proposals and a divergence report.

## Parts

| File | What it does |
|---|---|
| `case.py` | Case model (household, dwelling, costs, incomes, assets, date, expected outcome, unknowns). Built from the map's data objects. |
| `params.py` | Dated parameter sets with a source and verbatim quote per number. The case's decision date selects the set. |
| `rules/gha.py` | Rules as code, one function per rule family of the map. Each returns the value and the rule ids applied. Unknown facts raise, never guess. |
| `adapters/` | One interface per register the map names; a fixture implementation answers from the case; a real one would be read-only. |
| `runner.py` | Walks the map's nodes and edges. The automation class of each node decides who executes it: rule, registry, judge, gate, draft. Writes a step-by-step trace. |
| `synthetic.py` | A grid of synthetic households covering the rule branches. |
| `compare.py` | Compares a run with the real outcome and classifies the divergence. |
| `shadow.py` | Shadow mode: run a directory of mirrored cases, write a report for the process owner. |
| `cli.py` | `python -m twin.cli limits | grid | oracle | replay | shadow | case` from `process-mapper/`. |
| `tests/` | Kela's own worked examples as tests. |

## Stages and feeds

Each stage uses a feed of real outcomes that can be obtained before the next.

1. **Calculation against public oracles.** Kela's published income limits (36 values) and its online
   calculator. `python -m twin.cli limits`, `python -m twin.cli oracle twin/oracle/kela_calculator_results.json`.
2. **Full path on synthetic cases.** `python -m twin.cli grid`. Human gates return proposals, registers return fixtures.
3. **Replay against published appeal decisions.** `twin/cases/replay/` holds cases extracted from
   Social Security Appeal Board and Insurance Court decisions. `python -m twin.cli replay`.
4. **Shadow run with an agency.** `python -m twin.cli shadow <intake dir> <out dir>`: cases mirrored
   from a real intake, outcomes added when the real decision issues, a divergence report each week.
   Needs a partner and a data agreement; see `SHADOW.md`.

## What the twin is a twin of

Not Kela's internal routing. The validation study (`../research/assumption-1-validation.md`) showed
public documents give the rules, the order and the citizen-facing steps, and guess the internal
actors and automation. So the twin reproduces the decision function of the service and keeps the
map's internal steps as the sequence it walks, with each step marked by who executed it. Where the
map is wrong about the inside, the divergence report says so; the twin does not hide it.

## Plugging in a model

`runner.Judge` answers judgment and document-check nodes from the case's own facts. An LLM judge
with the same signature (node id, case, state -> Result) replaces it for cases that arrive as
documents rather than as structured facts. The gates (`human_signoff`, `human_only`) are enforced
by the runner, not by a prompt.
