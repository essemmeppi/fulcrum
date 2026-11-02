"""Build the national opportunity ledger and report from manually reviewed evidence.

Run from process-mapper: python -m survey.screening.build_report
Only the Python standard library is needed. Research judgements live in evidence.json.
"""

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
AREAS = {
    "social_services": "Social services",
    "revenue_business": "Revenue and business",
    "identity_rights": "Identity and rights",
    "land_environment": "Land and environment",
    "public_services": "Public services",
    "government_operations": "Government operations",
}
ORDER = {"strong_evidence": 0, "promising_evidence": 1, "public_facing_only": 2, "unknown": 3}
LABEL = {
    "strong_evidence": "Strong publication evidence",
    "promising_evidence": "Promising, unresolved detail/applicability",
    "public_facing_only": "Public-facing evidence inspected only",
    "unknown": "Unknown",
}


def main():
    countries = json.loads((HERE.parent / "registry/countries.json").read_text())["countries"]
    evidence = json.loads((HERE / "evidence.json").read_text())
    ids = {c["id"] for c in countries}
    assert len(ids) == len(countries) == 197
    assert all(e["country_id"] in ids and e["assessment"] in ORDER and e["area"] in AREAS for e in evidence)
    assert all(e["url"].startswith("https://") and e["government_level"] == "national" for e in evidence)
    rows = []
    for c in countries:
        matches = [e for e in evidence if e["country_id"] == c["id"]]
        assessment = min((e["assessment"] for e in matches), key=ORDER.get, default="unknown")
        detailed = [e for e in matches if e["assessment"] == "strong_evidence"]
        search = HERE / "searches" / f"{c['id']}.json"
        areas = HERE / "areas" / f"{c['id']}.json"
        row = {k: c[k] for k in ("id", "name", "region", "languages")}
        row.update(
            discovery_status="searched" if search.exists() else "not_searched",
            six_area_discovery="searched_not_exhaustively_verified" if areas.exists() else "not_searched",
            assessment=assessment,
            verification_status="selected_sources_reviewed" if matches else "not_verified",
            depth="detailed_operational_procedure" if detailed else (
                "some_internal_detail_or_unresolved_applicability" if assessment == "promising_evidence" else "unknown"
            ),
            verified_services=sorted({e["service"] for e in detailed}),
            verified_areas=sorted({e["area"] for e in detailed}),
            evidence=matches,
            discovery_log=f"searches/{c['id']}.json",
            area_search_log=f"areas/{c['id']}.json",
        )
        rows.append(row)
    (HERE / "countries.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    ledger = ["# All 197 national-government entries", "",
              "Initial discovery searches exist for every country; unknown means unresolved, not unsuitable. Breadth counts only individually inspected detailed examples. See report.md for interpretation and evidence.json for source limitations.", "",
              "| Country | Assessment | Observed depth | Detailed functions / areas | Evidence or verification lead |",
              "|---|---|---|---|---|"]
    for r in rows:
        best = sorted(r["evidence"], key=lambda e: ORDER[e["assessment"]])
        source = f"[{best[0]['title']}]({best[0]['url']})" if best else "Not verified"
        ledger.append("| " + " | ".join([
            r["name"], LABEL[r["assessment"]], r["depth"].replace("_", " "),
            f"{len(r['verified_services'])} / {len(r['verified_areas'])}", source,
        ]) + " |")
    (HERE / "countries.md").write_text("\n".join(ledger) + "\n")
    counts = Counter(r["assessment"] for r in rows)
    strong = [r for r in rows if r["assessment"] == "strong_evidence"]
    promising = [r for r in rows if r["assessment"] == "promising_evidence"]
    broad = [r for r in strong if len(r["verified_areas"]) >= 2]
    direct = [r for r in strong if any(e["assessment"] == "strong_evidence" and e["function_type"] == "external_service" for e in r["evidence"])]
    lines = [
        "# Worldwide national-government document screen", "", "Research date: 31 October 2026.", "",
        "**Initial discovery covers all 197 registry countries. Verification is partial. This is an evidence-supported lower bound, not an estimate of the complete addressable market.**", "",
        f"- **{len(strong)} countries**: detailed government-authored operational material inspected for at least one named national function.",
        f"- **{len(promising)} countries**: inspected material is promising, but depth, adoption or applicability remains unresolved.",
        f"- **{counts['public_facing_only']} countries**: public-facing evidence inspected only; internal-process evidence has not been established in this screen.",
        f"- **{counts['unknown']} countries**: unresolved. This includes unverified leads, access failures and weak search results; none is judged to lack useful data.",
        "",
        f"Of the strong group, **{len(direct)}** have an inspected citizen/business/community-facing or regulatory workflow. The other **{len(strong)-len(direct)}** currently qualify through enabling government operations such as procurement, personnel or document administration.",
        "",
        f"Verified detailed examples span at least two service areas in **{len(broad)} countries**: " + ", ".join(r["name"] for r in broad) + ". This is a minimum observed breadth; most countries have only one inspected example.",
        "",
        "## Wording suitable for EF", "",
        f"> We searched public sources across 197 countries and have so far verified detailed operational documentation from national authorities in at least {len(strong)}. The examples include "
        "business approvals, immigration, social services, relocation, emergency assistance, health administration and government operations. "
        "This establishes promising starting points for mapping and validation, not proof that whole governments can be mapped accurately or that workflows can already be executed.",
        "",
        "Do not turn the remaining unknowns into a negative result, infer revenue TAM, or describe this as 197 equally deep country assessments. Strong publication evidence can include historical editions; current legal and operational applicability still needs checking.",
        "",
        "## Depth and breadth", "",
        "Depth is the observed content of inspected documents. Breadth is the number of distinct named functions and areas with detailed evidence actually inspected. There is no composite score and no extrapolation from a national source to regions or municipalities.", "",
        "| Service area | Countries with detailed inspected evidence |", "|---|---:|",
    ]
    for area, label in AREAS.items():
        lines.append(f"| {label} | {sum(area in r['verified_areas'] for r in strong)} |")
    lines += ["", "Counts overlap across areas. These count publication opportunities, not verified complete maps.", "", "## Strong publication evidence", "",
              "Each example below has a source link and a locator in evidence.json. Dates are document editions where identifiable, not download dates. Historical and approval caveats remain attached.", "",
              "| Country | Named function | Area | Edition | Evidence inspected / limitation |", "|---|---|---|---|---|"]
    for r in strong:
        for e in r["evidence"]:
            if e["assessment"] != "strong_evidence":
                continue
            cells = [r["name"], f"[{e['service']}]({e['url']})", AREAS[e["area"]], e["document_date"], e["finding"] + " " + e["limitations"]]
            lines.append("| " + " | ".join(x.replace("|", "/").replace("\n", " ") for x in cells) + " |")
    lines += ["", "## Promising evidence requiring resolution", "", "| Country | Source | What remains unresolved |", "|---|---|---|"]
    for r in promising:
        for e in r["evidence"]:
            if e["assessment"] == "promising_evidence":
                lines.append(f"| {r['name']} | [{e['title']}]({e['url']}) | {e['limitations']} |")
    lines += ["", "## Limits and next verification work", "",
              "The baseline attempted one broad procedural-document query and six English-language area queries per country, supplemented by native-language searches in many countries. English results often contain unrelated countries or international reports. Those are not counted as national evidence. Language coverage and retrieval quality are uneven.", "",
              "Opened manual indexes and publication duties are leads, not operational evidence. A 403, timeout, certificate failure, missing page or PDF parsing failure describes this research client's access, not what the public or a normal browser can access. Some documents were recovered by ordinary direct download when the web reader had a size limit; no authentication was bypassed.", "",
              "Selected procedural sections were read, not every page of every manual. Costa Rica's blueprint was also inspected visually because extracted text omitted diagram content. All positive classifications still need an actual mapping trial and eventual government validation. Confidence scores, quote matches and prior model judges do not establish operational truth.", "",
              "Existing research and seven-layer country profiles were used as leads, not silently imported as verified country ratings. Publicly accessible existing disclosure copies qualify when government authorship is identifiable; the German example is hosted on a civil-society mirror. Subnational examples, including Mixco and Simeria, are excluded from the national count.", "",
              "Second verification pass (31 October 2026, evening): the saved discovery leads for the 163 countries left unresolved after the first pass were opened, up to four per country, by eight parallel agents working from the same classification rules. PDFs the web reader could not parse were downloaded by ordinary HTTP and read with pdftotext. Sites with broken TLS certificates were not bypassed; they stay unknown with the failure recorded. Eight documents judged strong but with only partial inspected depth were held as promising. Every record of that pass is in `verification-pass2-*.json`.", "",
              "Finish by verifying the strongest unresolved official manual links, recovering inaccessible documents through ordinary public routes, and adding individually inspected examples in under-covered areas. Do not launch an authority-by-authority census before this evidence justifies it.", "",
              "## Unresolved countries", ""]
    for region in sorted({r["region"] for r in rows}):
        names = [r["name"] for r in rows if r["region"] == region and r["assessment"] == "unknown"]
        lines.append(f"**{region}:** " + ", ".join(names) + ".\n")
    lines += ["## Files", "", "- `countries.md`: readable table of all 197 countries.", "- `countries.json`: all 197 country rows, search status, assessment, observed breadth and evidence.",
              "- `evidence.json`: manually reviewed source judgements, dates, locators and limitations.",
              "- `searches/` and `areas/`: exact discovery queries and raw results.",
              "- `verification-*.json` and `download-checks.json`: source access and inspection records.",
              "- `../METHOD.md`: method and counting rules.", ""]
    (HERE / "report.md").write_text("\n".join(lines))
    print(json.dumps({"countries": len(rows), "classifications": dict(counts), "direct_workflow_countries": len(direct), "multi_area_countries": len(broad)}, indent=2))


if __name__ == "__main__":
    main()
