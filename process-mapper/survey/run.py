"""Run the public-record survey with Claude and web tools.

Passes:
  country    one call per country in the registry     -> survey/countries/<iso2>.json
  authority  one call per authority in a country file -> survey/authorities/<iso2>/<id>.json
  service    one call per service in an authority file-> survey/services/<service_id>.json
             and services/<service_id>/sources.yaml for the mapper

Each call is one Claude turn with web_search and web_fetch, constrained to the pass's JSON schema.
Outputs that already exist are skipped, so a run can be resumed or extended. Validation is strict:
a file is written only if it parses into the schema.

Usage:
  python -m survey.run country                 # all countries
  python -m survey.run country fi it de        # some
  python -m survey.run authority fi            # every authority listed in survey/countries/fi.json
  python -m survey.run authority fi kela
  python -m survey.run service fi kela         # every service listed in survey/authorities/fi/kela.json
  python -m survey.run service fi-kela-general-housing-allowance
  python -m survey.run schema country          # print the JSON schema of a pass (for agents filling it by hand)

Options: --workers N (default 4), --model, --effort, --force (overwrite), --max-searches N
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from .schema import (AuthorityProfile, CountryProfile, ServiceSourceSet, scores_dict, tier_for)

ROOT = Path(__file__).resolve().parents[1]
SURVEY = ROOT / "survey"
PROMPTS = SURVEY / "prompts"
REGISTRY = json.loads((SURVEY / "registry" / "countries.json").read_text())["countries"]
BY_ID = {c["id"]: c for c in REGISTRY}

load_dotenv(ROOT / ".env")
MODEL = "claude-opus-5-5"
FETCHABLE = {"html", "pdf", "akn_xml", "ptv_api"}  # kinds mapper/fetch.py knows how to parse


def _tools(max_searches: int) -> list[dict]:
    return [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": max_searches},
        {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": max_searches * 2, "max_content_tokens": 40000},
    ]


def _json_schema(model: type[BaseModel]) -> dict:
    return model.model_json_schema()


def survey_call(client: anthropic.Anthropic, prompt: str, out_model: type[BaseModel], *,
                model: str, effort: str, max_searches: int) -> BaseModel:
    """One research turn: web tools plus a JSON-schema-constrained answer. Handles pause_turn."""
    messages = [{"role": "user", "content": prompt}]
    while True:
        with client.messages.stream(
            model=model,
            max_tokens=64000,
            output_config={"effort": effort, "format": {"type": "json_schema", "schema": _json_schema(out_model)}},
            tools=_tools(max_searches),
            messages=messages,
        ) as stream:
            msg = stream.get_final_message()
        if msg.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": msg.content})
            continue
        if msg.stop_reason == "refusal":
            raise RuntimeError("refusal")
        if msg.stop_reason == "max_tokens":
            raise RuntimeError("output hit max_tokens")
        break
    text = "".join(b.text for b in msg.content if b.type == "text")
    # With output_config.format the last text block is the JSON document; earlier text blocks (if any) are narration.
    last = [b.text for b in msg.content if b.type == "text"][-1]
    try:
        return out_model.model_validate_json(last)
    except ValidationError:
        return out_model.model_validate_json(text)


# --------------------------------------------------------------------------------------
# Pass runners
# --------------------------------------------------------------------------------------

def _stamp(obj: BaseModel, model: str) -> None:
    obj.surveyed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    obj.model = model


def run_country(client, country_id: str, args) -> Path:
    out = SURVEY / "countries" / f"{country_id}.json"
    if out.exists() and not args.force:
        return out
    c = BY_ID[country_id]
    prompt = (PROMPTS / "country.md").read_text().format(
        country_name=c["name"], country_id=country_id, region=f"{c['region']} / {c['subregion']}",
        languages=", ".join(c["languages"]) or "unknown",
    )
    prof = survey_call(client, prompt, CountryProfile, model=args.model, effort=args.effort, max_searches=args.max_searches)
    prof.country_id, prof.country_name = country_id, c["name"]
    _stamp(prof, args.model)
    out.write_text(prof.model_dump_json(indent=2))
    return out


def _country_summary(cp: CountryProfile) -> str:
    s = scores_dict(cp.layer_scores)
    lines = [f"tier {tier_for(s)}; layer scores {s}", cp.internal_guidance_practice]
    lines += [f"legal: {l.name} {l.url}" for l in cp.legal_information]
    lines += [f"catalogue: {c.name} {c.url}" for c in cp.catalogues]
    lines += [f"appeals: {a.name} {a.url}" for a in cp.appeals_sources]
    lines += [f"foi platform: {p.name} {p.url}" for p in cp.foi.disclosure_platforms]
    return "\n".join(x for x in lines if x)


def run_authority(client, country_id: str, authority_id: str, args) -> Path:
    out = SURVEY / "authorities" / country_id / f"{authority_id}.json"
    if out.exists() and not args.force:
        return out
    cp = CountryProfile.model_validate_json((SURVEY / "countries" / f"{country_id}.json").read_text())
    stub = next(a for a in cp.authorities if a.id == authority_id)
    prompt = (PROMPTS / "authority.md").read_text().format(
        country_name=cp.country_name, country_id=country_id, authority_name=stub.name,
        authority_id=authority_id, authority_url=stub.url, country_summary=_country_summary(cp),
    )
    prof = survey_call(client, prompt, AuthorityProfile, model=args.model, effort=args.effort, max_searches=args.max_searches)
    prof.country_id, prof.authority_id = country_id, authority_id
    _stamp(prof, args.model)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prof.model_dump_json(indent=2))
    return out


def _authority_summary(ap: AuthorityProfile) -> str:
    s = scores_dict(ap.layer_scores)
    lines = [f"tier {tier_for(s)}; layer scores {s}"]
    lines += [f"repository: {r.url} (enumerable={r.enumerable})" for r in ap.document_repositories]
    lines += [f"internal: {d.title} {d.url}" for d in ap.internal_documents[:20]]
    lines += [f"appeals: {a.name} {a.url}" for a in ap.appeals]
    return "\n".join(lines)


def export_sources_yaml(ss: ServiceSourceSet) -> Path:
    """Write services/<id>/sources.yaml in the mapper's format. Unfetchable kinds go to a comment block."""
    d = ROOT / "services" / ss.service_id
    d.mkdir(parents=True, exist_ok=True)
    country = BY_ID.get(ss.country_id, {}).get("name", ss.country_id)
    fetchable = [s for s in ss.sources if s.kind in FETCHABLE]
    other = [s for s in ss.sources if s.kind not in FETCHABLE]
    doc = {
        "service_id": ss.service_id,
        "service_name": ss.service_name,
        "country": country,
        "authority": ss.authority_name,
        "sources": [
            {"id": s.id, "title": s.title, "url": s.url, "kind": s.kind, "layer": s.layer,
             "publisher": s.publisher, "language": s.language}
            for s in fetchable
        ],
    }
    head = "# Public sources for one service, found by survey/run.py service. Layers: catalogue, legislation, guidance, forms, internal, statistics, appeals.\n"
    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120)
    tail = ""
    if other:
        tail = "\n# Found but not fetchable by mapper/fetch.py yet (kind not supported):\n" + "".join(
            f"#   - {s.id}  {s.kind}  {s.layer}  {s.url}\n" for s in other)
    p = d / "sources.yaml"
    p.write_text(head + body + tail)
    return p


def run_service(client, service_id: str, args) -> Path:
    out = SURVEY / "services" / f"{service_id}.json"
    if out.exists() and not args.force:
        return out
    country_id, authority_id = service_id.split("-", 2)[:2]
    ap = AuthorityProfile.model_validate_json((SURVEY / "authorities" / country_id / f"{authority_id}.json").read_text())
    stub = next(s for s in ap.services if s.id == service_id)
    cp = BY_ID[country_id]
    prompt = (PROMPTS / "service.md").read_text().format(
        country_name=cp["name"], country_id=country_id, authority_name=ap.name, authority_id=authority_id,
        authority_url=ap.url, service_name=stub.name, service_id=service_id, service_url=stub.url,
        authority_summary=_authority_summary(ap),
    )
    ss = survey_call(client, prompt, ServiceSourceSet, model=args.model, effort=args.effort, max_searches=args.max_searches)
    ss.service_id, ss.country_id, ss.authority_id, ss.authority_name = service_id, country_id, authority_id, ap.name
    _stamp(ss, args.model)
    out.write_text(ss.model_dump_json(indent=2))
    export_sources_yaml(ss)
    return out


# --------------------------------------------------------------------------------------

def main(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pass_", choices=["country", "authority", "service", "schema"])
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--effort", default="high")
    ap.add_argument("--max-searches", type=int, default=40)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    if args.pass_ == "schema":
        model = {"country": CountryProfile, "authority": AuthorityProfile, "service": ServiceSourceSet}[args.targets[0]]
        print(json.dumps(_json_schema(model), indent=2))
        return

    client = anthropic.Anthropic()
    jobs: list[tuple[str, callable]] = []
    if args.pass_ == "country":
        ids = args.targets or [c["id"] for c in REGISTRY]
        jobs = [(cid, lambda cid=cid: run_country(client, cid, args)) for cid in ids]
    elif args.pass_ == "authority":
        country_id = args.targets[0]
        cp = CountryProfile.model_validate_json((SURVEY / "countries" / f"{country_id}.json").read_text())
        ids = args.targets[1:] or [a.id for a in cp.authorities if a.delivers_services_to_public]
        jobs = [(f"{country_id}/{aid}", lambda aid=aid: run_authority(client, country_id, aid, args)) for aid in ids]
    elif args.pass_ == "service":
        if len(args.targets) == 2 and (SURVEY / "authorities" / args.targets[0] / f"{args.targets[1]}.json").exists():
            apf = AuthorityProfile.model_validate_json((SURVEY / "authorities" / args.targets[0] / f"{args.targets[1]}.json").read_text())
            ids = [s.id for s in apf.services]
        else:
            ids = args.targets
        jobs = [(sid, lambda sid=sid: run_service(client, sid, args)) for sid in ids]

    print(f"{args.pass_}: {len(jobs)} jobs, {args.workers} workers, model {args.model}")
    failed = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(fn): name for name, fn in jobs}
        for f in as_completed(futs):
            name = futs[f]
            try:
                print(f"  done {name} -> {f.result().relative_to(ROOT)}")
            except Exception as e:  # keep going; report at the end
                failed.append((name, repr(e)))
                print(f"  FAILED {name}: {e!r}", file=sys.stderr)
    if failed:
        print(f"{len(failed)} failed:", file=sys.stderr)
        for name, err in failed:
            print(f"  {name}: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
