# Replay cases: published appeal decisions on the general housing allowance

Each JSON file in this directory is a labelled real case extracted from a published appeal
decision on Kela's general housing allowance (yleinen asumistuki, Act 938/2014). The facts
come only from the decision text; every fact that matters to the outcome has a verbatim
Finnish quote in `source.quotes` (non-breaking spaces in the source were normalised to
plain spaces; nothing else was changed). Amounts the decision does not give are left at
the model default and listed in `unknowns`. Files were collected on 2026-11-01.

## Where the decisions came from

| Source | Searched | Found (post-2015, general housing allowance) | Files |
|---|---|---|---|
| Sosiaaliturva-asioiden muutoksenhakulautakunta (SAMU), decision database `https://www.samu.fi/ratkaisut_somla/` (keyword search `Asumistuki`, `Ruokakunta`, `Takaisinperintä`, `Asumismeno`, `Tulo`, `Tarkistaminen`) | 41 hits for `Asumistuki`, of which 12 dated 2015 or later; 3 of those concern the pensioners' housing allowance (Act 571/2007) and were left out | 9 | `samu-2017-01`, `samu-2019-01..03`, `samu-2020-01`, `samu-2021-01..03`, `samu-2024-01` |
| Vakuutusoikeus precedents, on Finlex (`/fi/oikeuskaytanto/vakuutusoikeus/<year>`, all pages for 2015-2026) and on `vakuutusoikeus.fi/ratkaisut/ratkaisujen-arkisto/` (search `asumistuki`) | 5 decisions keyworded asumistuki since 2015; 2 of them are pensioners' housing allowance (VakO 23596:2021, 1642:2025) and were left out | 3 | `vako-2019-01`, `vako-2020-01`, `vako-2025-01` |
| Korkein hallinto-oikeus on Finlex | Finlex's full-text search (`/fi/haku`) renders its results client-side and returned no result list to curl or headless Chromium; the KHO year listings were not crawled because housing-allowance appeals go to SAMU and the Insurance Court, not to KHO | 0 | - |
| Eduskunnan oikeusasiamies (`oikeusasiamies.fi`) | Unreachable: the site answers HTTP 403 with a Cloudflare challenge (`cf-mitigated: challenge`) to curl, and headless Chromium timed out on the challenge page | 0 | - |

Pre-2015 SAMU decisions (29 hits, 2008-2012) were applied under the old Housing Allowance
Act 408/1975 and were not extracted, since the twin models Act 938/2014 and selects its
parameter set from `decision_date`.

The raw pages are kept outside the repository in the session scratch directory
(`scratchpad/replay/`).

## What the cases cover

| File | Body, identifier | Dispute type | Outcome label |
|---|---|---|---|
| `samu-2017-01` | SAMU 20610/17/05 | household composition / residence: co-residents not covered by Finnish social security; only the applicant's share of rent accepted | revised |
| `samu-2019-01` | SAMU 10959/18/05 | income counting / interim revision: average income, 200 EUR decrease threshold not met, imputed labour market subsidy for a graduating student | granted (unchanged allowance) |
| `samu-2019-02` | SAMU 24265/18/05 | household composition: child in foster care over a year is not a temporary absence | revised |
| `samu-2019-03` | SAMU 22828/18/05 | income counting: summer job lasting three months is continuous income, not averaged | revised |
| `samu-2020-01` | SAMU 31494/19/05 | household composition: minor living alone without sufficient income belongs to the parents' household | rejected |
| `samu-2021-01` | SAMU 22454/21/05 | start date: entitlement begins the month after a lease starting mid-month | granted |
| `samu-2021-02` | SAMU 21008/21/05 | household composition (alternating residence child) and disability extra-space; full calculation shown (Lapua, group 4, 3 persons, 2021 parameters) | granted (193,30 EUR) |
| `samu-2021-03` | SAMU 10923/21/05 | income counting: entrepreneur income at YEL confirmed income; labour market subsidy counted | revised |
| `samu-2024-01` | SAMU 29667/23/05 | income counting: share-savings-account capital gains as recurring gross income; termination at annual review | terminated |
| `vako-2019-01` | VakO 716:2019 | correction to detriment / termination / recovery: s. 38(2) consent requirement | granted (original 243,41 EUR stands) |
| `vako-2020-01` | VakO 2361:2020 | eligible dwelling and housing costs: group-home room under a lease | revised (rejection annulled, returned to Kela) |
| `vako-2025-01` | VakO 1168:2023 | recovery: five-year limit applies separately to each jointly liable household member | revised (recovery against spouse time-barred) |

Distribution: household composition 4 (one overlapping with residence), income counting 5
(one overlapping with revision thresholds), recovery / correction to detriment 2, eligible
dwelling and housing costs 2 (one overlapping with household composition), start date 1,
termination 1.

### Outcome label convention

`expected.outcome` is the final result as it applies to Kela's decision:

- `granted`: an allowance is due; `monthly_allowance` is filled when the decision states it.
- `rejected`: no entitlement.
- `terminated`: the allowance ends from the stated date.
- `revised`: the appeal body changed or annulled Kela's decision, or upheld a Kela revision,
  without a final monthly amount being stated; `reason` says what changed.
- `recovery` is reserved for cases where an overpayment is finally ordered to be recovered;
  none of the collected cases ends that way (both recovery cases set the recovery aside).

## What the decisions typically do not state (limits for the twin)

- **Rent and other housing costs.** Only 3 of 12 decisions give the rent (200, 828 and
  1 027 EUR); none says whether water or heating is paid separately or whether the rent
  includes electricity or excluded fees. Most cases can therefore test an eligibility,
  household or income-counting step but not the full amount.
- **Municipality and municipality group.** Stated in one case (Lapua, group 4). Region for
  heating flat rates is never stated.
- **Ages.** Never stated directly; one age is derived from a stated birth month. Children are
  described only as minors.
- **Household size.** Several SAMU summaries name only the applicant and speak of "the
  household"; the number of members is left unknown where it is not stated.
- **Complete income picture.** Decisions quote only the income item in dispute. Where a
  figure is annual (YEL income, capital gains) the monthly figure in the file is the annual
  figure divided by 12, and the note says so. Assets are never mentioned.
- **The resulting allowance.** Only 3 decisions state a monthly amount (30,96; 193,30;
  243,41 EUR). SAMU summaries end with "rejected" or "changed" and rarely show the
  recalculation; VakO 2361:2020 returns the case to Kela without deciding the amount.
- **Procedural facts the model has no field for**: alternating residence of a child,
  foster-care placement, a lease starting mid-month, limitation periods for recovery,
  consent to correction of a final decision. These are recorded in `notes`, `reason` and
  `unknowns`; the twin will need rules or human questions for them.
- **Typos in the source** are quoted as printed (e.g. "l.6.2019", "17.2023 – 30.6.2023",
  "Kansanelälaitos") and explained in the notes.
