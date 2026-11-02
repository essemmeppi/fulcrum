# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences, confirmed by Simone on 2026-11-02, in this order for the next few months:

1. **Programme, funders and investors.** The EF/BlueDot Fulcrum cohort and anyone deciding whether to back The Agentic State as a venture. Their situation: a short look at the site and the demo, often on a phone, between other pitches. Their job: decide whether the thesis is credible, whether the evidence is real, and whether the team can reach a government.
2. **Government process owners.** The team inside one agency (a benefit unit at Kela, a municipal secretariat like Deta) that would let the work happen: hand over documents, correct a map, agree to a shadow run. Their job: judge whether the map of their own service is accurate enough to be worth correcting, and whether the twin is safe to let near real cases. Their engagement is the proof the first audience is looking for.

Peers and researchers (govtech, rules-as-code, digital government) read the work but were not selected as an audience to design for.

## Product Purpose

The Agentic State makes government processes legible to machines, operable by agents, and accountable to people. It reads the public record of a public service (statutes, guidance, forms, decision templates, internal instructions, reports) and compresses it into a map: steps, actors, rules, data sources and flows, each tied to the passage it comes from, with a confidence score. The map becomes the specification an agent harness loads (encode), and later the basis for redesigning the process with the authority (redesign). Map, encode, redesign is the product's sequence and the structure of its site.

**Success for the next few months (confirmed 2026-11-02):** funding or programme selection. The venture is judged on whether its evidence holds and whether a government will engage; a first agency shadow run is the next proof, not the current goal.

## Positioning

The mechanism a neighbouring product cannot truthfully copy: whole-service maps built from **public documents only**, without interviews or access to internal systems, where every element carries **provenance** (source, section, verbatim quote, exact-match verified) and a **confidence** figure from a fixed rubric, and the structure is the same for every service in every country. What is not documented is marked inferred, not smoothed over. The map is not a diagram for a workshop: the same JSON is loaded by the twin, which reproduces the service's decision function, replays real published outcomes, and reports where the map is wrong about the inside.

Contrast, as discussed in the programme: process-observation startups map organisations by watching people at computers; consultancies rebuild processes from interviews and workshops. Both need the organisation's cooperation before the first drawing. This approach starts before cooperation and uses cooperation to validate.

## Operating Context

- **Programme.** One-week EF/BlueDot Fulcrum sprint, week of 2026-10-27. Feedback calls recorded from James Savage (EF, 2026-10-27) and Luukas Ilves (2026-10-30); transcripts in `chats/`, gitignored and private.
- **Site.** Static HTML, no build step, served by GitHub Pages from `main` → `/docs` at https://essemmeppi.github.io/fulcrum/ (repo https://github.com/essemmeppi/fulcrum). Three pages: landing (`docs/index.html`), Kela demo (`docs/fi-kela-general-housing-allowance.html`), Deta municipal study (`docs/ro-tm-deta.html`). `share/the-agentic-state.html` is a generated single-file bundle (`python3 -m mapper.bundle` from `process-mapper/`), never hand-edited.
- **Pipeline.** `process-mapper/`: `mapper/` (fetch → extract facts with verbatim quotes → verify → synthesise map JSON → render), `twin/` (parallel system: rules as code, dated parameters, register adapters, runner, synthetic grid, replay, shadow mode; `python -m twin.cli`), `survey/` (country / authority / service screening of the public record), `research/` (validation study, twin note). Model used for extraction: `claude-opus-5-5`.
- **Working method.** Simone edits the `docs/` pages by hand in VS Code; they are the source of truth. `mapper.render` only replaces the `const DATA = …;` line. Codex works on the same repo alongside Claude Code; `survey` is the integration branch for research. Simone works step by step and reviews each result before the next; outputs must be understandable by externals.
- **Contact.** hello@agenticstate.org.

## Capabilities and Constraints

**Vocabulary (fixed, use exactly):** service (CPSV-AP words) → has processes; process = as-is steps; workflow = agent-operable encoding; step (event · task · decision, BPMN words); actor (drawn as a lane); rule (defined once per service, referenced by steps; kinds eligibility · calculation · procedural · deadline · sanction); input; data source; channel; **provenance** (never "evidence" or "citation" for the per-element record); grounding = documented · inferred; external · internal (step attribute); **confidence** (expected probability a step matches reality, fixed rubric) with a human `validated` flag; agent mode = execute · prepare for a human · human only. Always "process", never "procedure". Standards (CPSV-AP, BPMN) are vocabulary anchors only; nothing is implemented against them.

**What exists:** one map schema used across countries (`mapper/schema.py`); the Kela map and page; the Deta study and page; the 197-country screen; the twin through stage 4 (shadow mode demonstrated on mirrored synthetic intake, no agency partner). The twin never acts on a citizen, a register or a payment: every mode produces proposals and a divergence report; human gates are enforced by the runner, not by a prompt.

**Known source limits:** Finlex consolidated text of Act 938/2014 stops at amendment 12/2017, so 2024–25 parameter changes come only from Kela guidance (the map flags the conflict). Kela's full internal benefit guidelines are not public; one internal procedure note (automated termination) is. PTV service catalogue is thin for Kela. Deta passages were referenced manually without quote verification.

**Open decisions (recorded, not invented):**
- Business model. Discussed in the cohort on 2026-10-28: open-source the mapping engine, earn on forward-deployed work (validation, agent deployment, redesign), likely customer one agency rather than a whole government; EF pushed for-profit. None of this is confirmed as a commitment or published.
- Whether and where the name "Fulcrum" appears publicly. Confirmed 2026-11-02: the product and venture name is The Agentic State; Fulcrum is the programme only. The research one-pager still says "Fulcrum aims to…" and the GitHub repo is named `fulcrum`.
- No accessibility standard has been chosen.
- No pricing, licensing, customer or deployment claims exist; none may be implied.

## Brand Commitments

- **Name:** The Agentic State. Mission line on the site: "Making government legible to machines, operable by agents, and accountable to people."
- **Voice:** flat thesis prose. No slogans, no catchy taglines, no SaaS-speak (Simone rejected "Government is written down. It has never been written to run."). Findings are stated with their limits in the same breath; classifications are called classifications, not measurements. Plain explanations over method detail for externals.
- **Register references Simone made binding:** observableintuition.com and readystatelabs.org/About (narrow reading column, prose first).
- **Visual constraints volunteered by Simone, recorded without expansion:** Newsreader (italic, light) with Inter; accent #8b7ae8; light and dark themes already in the pages; favicon set in `docs/favicon/`. The three `docs/` pages are the incumbent and are hand-edited; a template re-render once overwrote hero copy and had to be recovered, so no regeneration of these files.

## Evidence on Hand

Real, with paths. Nothing here is government-validated; say so wherever it is shown.

- **Kela general housing allowance map** (Finland, Act 938/2014), mapped 2026-10-28: `process-mapper/maps/fi-kela-general-housing-allowance/map.json`, page `docs/fi-kela-general-housing-allowance.html`. 8 public sources, 818 facts, 100% of quotes verified, 84 steps, 95 flows, 79 rules, 13 data sources, 10 actors, 16 open questions, 95% of facts used as provenance, mean confidence external 0.85 vs internal 0.72, 1 inferred step. Not validated by Kela.
- **Twin** (`process-mapper/twin/`): 28 of 28 Kela calculator runs reproduced; 36 published income limits matched; 12 published appeal decisions (Social Security Appeal Board, Insurance Court) replayed from `twin/cases/replay/`; two-phase shadow-mode demonstration. No agent has run on a real case; no agency partner.
- **Validation study** `process-mapper/research/assumption-1-validation.md`: public documents give the rules, the order and the citizen-facing steps, and guess the internal actors and automation.
- **Worldwide screen** of 197 countries (research 2026-10-31, summary 2026-11-01): `output/research/one-pager.md`, map `output/research/worldwide-findings.svg|png|html`, ledger `process-mapper/survey/screening/countries.md`, method `process-mapper/survey/METHOD.md`. 86 countries with detailed operational material, 41 promising but unresolved, 20 public-facing only, 50 unknown. A lower bound on publication, not a market estimate.
- **Deta, Romania municipal study** (CDIT member municipality): page `docs/ro-tm-deta.html`, data in `work/cdit-export/` (gitignored, regenerated by `build_portfolio.py`). 10 mapped processes, 52 identified, 24 documents read. Manual passages, no quote verification, no municipal endorsement.
- **Absent, must not be fabricated:** customers, testimonials, pilots, government validation, pricing, logos of partners, measured agent performance on real cases, benchmarks against other tools.

## Product Principles

1. **The public record is the source, and its gaps are shown.** Every element points to a passage; what has none is marked inferred and scored, never filled in. Access to internal documents raises confidence; it is asked for, not assumed.
2. **Claims match what was done.** A classification is not a measurement; a screen is a lower bound; a replay is not a pilot. Each finding carries its limit next to it, because the audiences are judging credibility.
3. **Humans decide; the twin proposes.** Nothing acts on a citizen, a register or a payment. Gates are in code. The map is the agenda for a conversation with the process owner, not a verdict on them.
4. **One structure for every service in every country.** Maps are comparable and machine-loadable; the same JSON drives the page, the twin and the redesign.
5. **Plain prose, few files.** Outputs are understandable by funders and officials without method detail. Add structure only when a result demands it; the fear is overengineering.
