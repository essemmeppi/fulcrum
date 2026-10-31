# Public-record survey

**Current national opportunity research:** [results and limits](screening/report.md) · [all 197 countries](screening/countries.md). The seven-layer pipeline below is legacy scaffolding, not the current opportunity-counting method.

Answers one question before any mapping is attempted: for which governments, authorities and
services could an accurate process map be built from public documents alone, without the
government's cooperation?

Start with [METHOD.md](METHOD.md) for the scope, thresholds, discovery protocol and counting rules.
The mapper (`mapper/`) measures source grounding, not operational truth. This survey screens
publication availability; only a service-level mapping exercise tests whether those sources support
a map. Government validation remains a separate later stage.

Current coverage is partial. National profiles must not be extrapolated to regions, municipalities,
all agencies, or all services. The report includes all 197 registry entries in `coverage.csv`, with
unsurveyed countries explicitly unknown. Existing profiles are preliminary and not independently
reverified. Regional and municipal inventories have not yet been built.

## Three passes

| Pass | Unit | Output | What it establishes |
|---|---|---|---|
| country | each of 197 countries in `registry/countries.json` | `countries/<iso2>.json` | legal database and its format, service catalogue, FOI regime and proactive-publication duties, internal-guidance practice, appeals, audit, statistics, procurement, rules-as-code; the list of national authorities to survey |
| authority | every service-delivering national authority named by the country pass | `authorities/<iso2>/<id>.json` | document repositories and whether they are enumerable; published staff instructions and procedure manuals; forms, statistics, appeals, audit, FOI releases, tender documents; the list of services |
| service | every service named by the authority pass | `services/<service_id>.json` and `../services/<service_id>/sources.yaml` | every public document describing the service, ready for `mapper.fetch` |

Whether an authority publishes internal instructions is a property of the authority, not of the
service, which is why the middle pass exists: a few thousand authority surveys predict the internal
layer for every service they run.

## Layers and scores

The seven layers are the ones `sources.yaml` already uses. Each pass scores every layer 0-3:

| Score | Meaning |
|---|---|
| 0 | nothing found |
| 1 | exists for some services or is hard to reach |
| 2 | systematic for the main authorities or services, reachable by browsing |
| 3 | systematic and enumerable or machine-readable |

The tier is computed in code (`schema.tier_for`), never by the model:

| Tier | Condition | Expected map |
|---|---|---|
| 0 | law or guidance not found | insufficient evidence found, not proof of impossibility |
| 1 | law and guidance | external skeleton candidate |
| 2 | plus forms, and appeals or catalogue | external process candidate |
| 3 | plus internal >= 2, and statistics or appeals >= 2 | internal mapping candidate; needs service-level testing |
| 4 | tier 3 plus layer scores >= 3 for law and catalogue | structured-source candidate; refreshability untested |

What the Finland map showed about source value, and what the prompts therefore prioritise:
legislation carried most internal-step provenance and nearly all flows; guidance carried most rule
parameters; forms carried inputs; the single internal procedure note was the only source of
automation facts. Statistics and appeals were absent and the open questions are exactly what they
answer. Translations of one page count as one source.

## Running

Each unit is one Claude turn with web search and web fetch, constrained to the pass's JSON schema,
validated, and written only if it parses. Existing outputs are skipped, so runs resume.

    python -m survey.run country                      # every country
    python -m survey.run country fi it de
    python -m survey.run authority fi                 # every authority in countries/fi.json
    python -m survey.run service fi kela              # every service in authorities/fi/kela.json
    python -m survey.run schema country               # JSON schema, for filling a unit by hand or by another agent
    python -m survey.validate country fi              # check and normalise a file
    python -m survey.report                           # report.md and report.csv

`ANTHROPIC_API_KEY` in `process-mapper/.env`. Default model `claude-opus-5-5`, effort high, 40 searches per unit.

A unit can also be filled by any agent with web access: give it `prompts/<pass>.md` with the
placeholders substituted and `registry/<pass>.schema.json`, have it write the file, and run
`survey.validate` on the result. The first wave of country files was produced this way.

## Reading the output

`report.md` lists countries by tier and by region, the seven layer scores per country, and the
authorities and services surveyed so far. `report.csv` has the same per-country rows for analysis.
Every score in a country file carries `evidence_urls`; every system named carries a URL that was
opened. "Not found" is recorded as such, with what was searched, in `notes` or `open_questions`.
