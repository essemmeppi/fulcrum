# Expanded municipal research

Start with [FINDINGS.md](FINDINGS.md) for the expanded pass: 10 partial workflow sheets across eight families, 87 source-located action claims, 52 provisional families/leads and seven search targets. The initial screen below is retained as research history; the new portfolio supersedes its coverage assessment.

No workflows are municipality-validated. Current local grant evidence has now been read; the earlier statement that no local operational procedure was inspected no longer describes the expanded pass. The old information-access ledger remains an initial snapshot; use `deta-portfolio.json` for the amended national norms.

Rebuild generated files with `python build_portfolio.py` from this directory. The builder validates IDs, source references and explicit links. It does not perform independent quote verification.

---

# CDIT municipal mapping pilot for ADR Vest

Screen date: 2026-10-31. Research baseline: `1e67353d1455dbedc5950ffe0fd3cfae5777c0ac`.
Scope: CDIT member town halls in Timiș, with findings used to inform ADR Vest's regional digitalisation strategy. This is a separate municipal study, excluded from the national opportunity counts in `survey/METHOD.md`.

## Decision now

Start a provisional whole-town-hall inventory for **Deta**, then reconstruct one bounded service: public-information requests and their administrative complaints under Law 544/2001. Deta is a confirmed CDIT member and its electronic catalogue is readable. This is an initial choice based on inspected material, not a ranking of all 22 members. A process owner nominated by CDIT can change the choice.

The catalogue supplies 29 form entries, grouped here into 22 provisional process families. These are discovery candidates, not 22 validated workflows. A general request form is an intake channel, not a claim that all municipal functions have been enumerated. Back-office processes require a separate search.

## What the latest research changes

Read with `../../../research/assumption-1-validation.md`, particularly sections 2.5, 4 and 5, and `../../METHOD.md`.

- Extract a claim ledger; leave desk actors, automation and order unknown when sources are silent. Do not force a complete graph.
- Read operational procedures first when available, followed by implementing norms, law, local guidance, forms, catalogue and secondary material. Rank for reading efficiency; apply precedence separately to each claim.
- Distinguish legal responsibility from the person doing the work. A mayor's legal responsibility does not establish that the mayor performs a desk task.
- Count independent evidence, not URLs. Translations, reprints and the same law copied onto municipal websites share an evidence origin.
- Preserve contradictions, superseded claims, and the additions/confirmations/refinements attributable to each document.
- The earlier Romanian experiment is methodological evidence only. No other town's routing, staffing or software is imported into Deta.
- Earlier model-judged recall is not a forecast for this municipality; human review remains unperformed.

## Evidence quality and time

Use an evidence profile rather than an arbitrary weighted score. Store publisher, jurisdiction, document purpose, procedural depth, publication/adoption/effective dates, repeal/supersession, observation date, independence group and access status.

Prefer an applicable adopted local procedure for desk routing; applicable legislation for legal duties; dated local guidance for season-specific arrangements; actual case traces for observed execution. None substitutes for the others. A new draft does not displace an adopted rule. A fetched-at date does not make an old document current. A newer guidance parameter that conflicts with law is a conflict requiring amendment/version checks, not permission to override law automatically.

Read every accessible source and record marginal yield. Low-ranked documents can add genuine exceptions. Unknown dates and unresolved legal versions block claims of current operational validity, not extraction of clearly labelled historical evidence.

## What has actually been checked

CDIT lists 22 cities/communes plus Timiș County. Timișoara is not on that published list. All members are in `screen.json`; only three have received any local screening here.

| Candidate | Evidence inspected | Result and limitation |
|---|---|---|
| Deta | organisation page, electronic catalogue, information-access page, social-assistance pages | Public-facing evidence, plus leads to ROF, reports and forms. Word attachments could not be read by the web reader; electronic form links redirect to login. No local operational procedure inspected. |
| Dumbrăvița | ROF PDF URL | Access challenge returned instead of document. Indexed metadata is a lead only. |
| Traian Vuia | social-assistance index | Dated output titles and links to organisational/information-access material; attached decisions not inspected. An index is not operational evidence. |

No six-area municipal screen is complete. For Deta: social services and revenue/business have catalogue-level evidence; land/environment has urbanism entries only; government operations has a public-information entry. Identity/rights and education/health/utilities have not been substantively checked. Organisational navigation is a lead, not verified service evidence. No strong internal-process classification is assigned.

## First process: evidence and review, not a finished blueprint

`deta-information-access.json` contains a small source-backed intake/complaint ledger and open questions. It deliberately has no inferred internal sequence, automation assignment or legal deadline copied from a search snippet. The official legislative portal returned Arts. 3–4 and a 10 May 2024 consolidation label on one attempt, but failed on follow-up. A readable official-agency copy of HG 123/2002 supplies a historical internal-process skeleton. Its old deadline wording illustrates why version reconciliation matters. Full current law and norms still need versioned acquisition. The three electronic form URLs were followed and all redirected to login. No account was created and nothing was submitted.

Next acquisition: the local ROF; the Law 544 request/complaint form contents; the 2023 implementation report and newer reports if available; current Law 544 and HG 123 implementing norms; any published local procedure, records schedule, audit findings and redacted decisions. Enumerate attachments before concluding that procedures are absent. Word documents need download/conversion, not an absence label.

Then read sequentially into the ledger, retain rules apart from actions, verify quotes and explicit order against source snapshots, and produce a review sheet with: we do this / differently / we do not / ask this person. Measure new claims, refinements, conflicts, independent support and time spent reviewing. Add the procedure at the top when CDIT supplies it; its incremental contribution is a deliverable.

## From one service to the town hall

Reconcile (1) ROF responsibilities and organisational units, (2) service/form/output catalogues, and (3) internal operational-procedure registers. Cover citizen services and enabling processes: registry, finance/payments, procurement, HR, legal work, records and IT. These enabling families are search targets, not confirmed Deta processes in this screen.

Keep an inventory row per process family with variants, boundaries, owner evidence, sources, last effective version, internal depth and review status. Shared national rules can be reused across CDIT, but local actors, handoffs, software and timing must remain municipality-specific. Report coverage against the reconciled inventory; do not claim 'all processes' from the portal alone.

## What to ask Dan

1. Confirm the current CDIT membership and nominate one member with a willing secretary general and service owner.
2. Share the digital-maturity questionnaire and an anonymised result export. CDIT says collection ran 14–30 October, with results to be presented 10 November. Responses are not public and have not been read here.
3. Obtain that town hall's process/procedure register, current ROF and organigram, one operational procedure, relevant forms, software list and a few redacted completed cases. Ask for volume, handling time and rework separately; none is known yet.
4. For ADR Vest, confirm the precise funding line, current uncommitted amount, applicant/partnership eligibility, procurement route and whether mapping/diagnostic work is eligible. Its public summary gives EUR 18.76m and encourages interoperable, replicable pilots; it is not a current call guide. It lists counties, municipalities and towns, so eligibility of commune members or a CDIT-led partnership must not be assumed.

The strategic output is a portfolio of evidenced needs and reusable process families, with local differences and confidence limits. Prioritise investments only after adding demand, pain, readiness and cost evidence; document availability alone is not investment value.

## Sources and limits

See `screen.json` for URLs, access outcomes and dates, and `deta-process-inventory.csv` for provisional families. This is a bounded desk-research screen, not a completed mapper run, a digital-maturity assessment, or agency validation. No changes to the national survey, mapper or existing research were made.

## Legislative inputs are central

For each municipal process, assemble a legal bundle: applicable national statute, implementing government decisions/ministerial orders, relevant EU requirements where applicable, county-level acts where competent, local council decisions, mayoral dispositions, and local ROF/procedures. Inspect each act's authority and territorial/material scope rather than assigning weight from geography alone. No freestanding regional legislative layer is assumed for Regiunea Vest; ADR Vest programme rules concern financing and must be tracked separately from municipal service duties.

National implementing norms can expose internal work, not just eligibility. In the inspected historical HG 123 copy, Arts. 20–24 describe registration, primary assessment, internal routing, drafting and dispatch. Art. 4 of Law 544 explicitly points to the authority's ROF. This provides a common legal skeleton across CDIT and a precise local-document acquisition agenda. It does not prove Deta performs each step as written or uses any particular software.

Version example: the CNCAN-hosted historical norms copy says working days in Art.16. Do not use that copy to configure current timers. Publication on an official site and a recent crawl date establish neither amendment completeness nor current legal effect.
