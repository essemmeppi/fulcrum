# Public-record survey

Answers one question before any mapping is attempted: for which governments, authorities and
services could an accurate process map be built from public documents alone, without the
government's cooperation?

The mapper (`mapper/`) is the measurement of record: a map's `report.json` says how many internal
steps were documented, at what confidence, and what stayed open. This survey predicts that outcome
cheaply for every national government, so the mapper can be pointed where it will succeed, and so the
rest can be counted as unmappable without further work. No sampling, no extrapolation: every
country, every national authority, every service they list.

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
| 0 | law or guidance missing | none |
| 1 | law and guidance | external steps documented, internal steps inferred |
| 2 | plus forms, and appeals or catalogue | full external process, rules with parameters |
| 3 | plus internal >= 2, and statistics or appeals >= 2 | internal steps documented (the Finland case) |
| 4 | tier 3 plus machine-readable law and catalogue API | map can be refreshed automatically |

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
