"""Aggregate survey outputs into survey/report.md and survey/report.csv.

Usage:
  python -m survey.report
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

from .schema import LAYERS, TIER_LABELS, AuthorityProfile, CountryProfile, ServiceSourceSet, scores_dict, tier_for

ROOT = Path(__file__).resolve().parents[1]
SURVEY = ROOT / "survey"
REGISTRY = json.loads((SURVEY / "registry" / "countries.json").read_text())["countries"]


def load_countries() -> dict[str, CountryProfile]:
    out = {}
    for p in sorted((SURVEY / "countries").glob("*.json")):
        out[p.stem] = CountryProfile.model_validate_json(p.read_text())
    return out


def load_authorities() -> list[AuthorityProfile]:
    return [AuthorityProfile.model_validate_json(p.read_text()) for p in sorted((SURVEY / "authorities").glob("*/*.json"))]


def load_services() -> list[ServiceSourceSet]:
    return [ServiceSourceSet.model_validate_json(p.read_text()) for p in sorted((SURVEY / "services").glob("*.json"))]


def main() -> None:
    countries = load_countries()
    authorities = load_authorities()
    services = load_services()
    by_country = {c["id"]: c for c in REGISTRY}

    rows = []
    for cid, cp in countries.items():
        s = scores_dict(cp.layer_scores)
        rows.append({"country_id": cid, "country": cp.country_name, "region": by_country.get(cid, {}).get("region", ""),
                     "tier": tier_for(s), **s, "authorities_listed": len(cp.authorities),
                     "procedure_publication_duty": cp.foi.procedure_publication_duty,
                     "catalogue_api": any(c.machine_readable for c in cp.catalogues),
                     "law_api": any(l.machine_readable for l in cp.legal_information)})
    rows.sort(key=lambda r: (-r["tier"], -sum(r[l] for l in LAYERS), r["country"]))

    with (SURVEY / "report.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["country_id"])
        w.writeheader()
        w.writerows(rows)

    tiers = Counter(r["tier"] for r in rows)
    regions = {}
    for r in rows:
        regions.setdefault(r["region"], Counter())[r["tier"]] += 1

    md = ["# Public-record survey: national level", "",
          f"Countries surveyed: {len(rows)} of {len(REGISTRY)}. Authorities surveyed: {len(authorities)}. Services surveyed: {len(services)}.", "",
          "## Countries by tier", "", "| Tier | Meaning | Countries |", "|---|---|---|"]
    for t in range(4, -1, -1):
        names = ", ".join(r["country"] for r in rows if r["tier"] == t)
        md.append(f"| {t} | {TIER_LABELS[t]} | {tiers.get(t, 0)}: {names} |")
    md += ["", "## By region", "", "| Region | " + " | ".join(f"T{t}" for t in range(5)) + " |", "|---|" + "---|" * 5]
    for reg, c in sorted(regions.items()):
        md.append(f"| {reg} | " + " | ".join(str(c.get(t, 0)) for t in range(5)) + " |")
    md += ["", "## Layer scores", "", "| Country | Tier | " + " | ".join(LAYERS) + " | Procedure publication duty | Law API | Catalogue API |",
           "|---|---|" + "---|" * (len(LAYERS) + 3)]
    for r in rows:
        md.append(f"| {r['country']} | {r['tier']} | " + " | ".join(str(r[l]) for l in LAYERS) +
                  f" | {'yes' if r['procedure_publication_duty'] else ''} | {'yes' if r['law_api'] else ''} | {'yes' if r['catalogue_api'] else ''} |")

    if authorities:
        md += ["", "## Authorities", "", "| Country | Authority | Tier | internal | services listed |", "|---|---|---|---|---|"]
        for a in sorted(authorities, key=lambda a: (a.country_id, a.authority_id)):
            s = scores_dict(a.layer_scores)
            md.append(f"| {a.country_id} | {a.name_en or a.name} | {tier_for(s)} | {s['internal']} | {len(a.services)} |")
    if services:
        md += ["", "## Services", "", "| Service | Tier | sources | internal sources |", "|---|---|---|---|"]
        for s_ in services:
            s = scores_dict(s_.layer_scores)
            md.append(f"| {s_.service_id} | {tier_for(s)} | {len(s_.sources)} | {sum(1 for x in s_.sources if x.layer == 'internal')} |")

    (SURVEY / "report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:12]))
    print(f"\nwrote {SURVEY / 'report.md'} and report.csv")


if __name__ == "__main__":
    main()
