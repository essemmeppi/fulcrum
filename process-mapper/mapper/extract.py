"""Turn a fetched corpus into an provenance-backed process map.

Two passes with Claude, then deterministic verification:

  Pass A  (per source, in parallel)  source text  -> FactSheet   atomic claims + verbatim quotes
  verify  (code)                     each quote exact-matched against the source text; unverifiable quotes are dropped
  Pass B  (one call)                 all verified facts -> ProcessMap   nodes/edges/rules cite fact ids
  expand  (code)                     fact ids -> Passage objects; grounding = documented / inferred

Outputs in maps/<service_id>/: facts.json, map.json, report.json

Usage:
  python -m mapper.extract services/fi-kela-general-housing-allowance
"""

import json
import os
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from .schema import Passage, Fact, FactSheet, ProcessMap, Source

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "mapper" / "prompts"
MODEL = "claude-opus-5-5"

load_dotenv(ROOT / ".env")
if not os.environ.get("ANTHROPIC_API_KEY"):
    # The sister project keeps the key next door; reuse it rather than copying secrets around.
    load_dotenv(ROOT.parents[1] / "tasks" / ".env")

client = anthropic.Anthropic()


# --------------------------------------------------------------------------------------
# Pass A: facts per source
# --------------------------------------------------------------------------------------

CHUNK_CHARS = 22000  # a law of 40K chars yields more facts than fit in one output; chunk at marker lines


def split_text(text: str, max_chars: int = CHUNK_CHARS) -> list[str]:
    """Split on locator-marker lines ('[...]') so every chunk starts with a marker the model can cite."""
    if len(text) <= max_chars:
        return [text]
    chunks, cur, last_marker = [], [], ""
    size = 0
    for line in text.splitlines():
        is_marker = line.startswith("[")
        if is_marker and size > max_chars and cur:
            chunks.append("\n".join(cur))
            cur, size = [], 0
        if is_marker:
            last_marker = line
        elif not cur and last_marker:
            cur.append(last_marker)  # carry the current section marker into the new chunk
        cur.append(line)
        size += len(line) + 1
    if cur:
        chunks.append("\n".join(cur))
    return chunks


def _facts_call(source: Source, text: str) -> FactSheet:
    prompt = (PROMPTS / "facts.md").read_text()
    user = prompt.format(
        source_id=source.id, title=source.title, publisher=source.publisher,
        layer=source.layer, language=source.language, url=source.url, text=text,
    )
    with client.messages.stream(
        model=MODEL,
        max_tokens=48000,
        output_config={"effort": "high"},
        messages=[{"role": "user", "content": user}],
        output_format=FactSheet,
    ) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        raise RuntimeError(f"refusal on {source.id}")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError(f"{source.id}: output hit max_tokens with a {len(text)}-char chunk; lower CHUNK_CHARS")
    raw = next(b.text for b in msg.content if b.type == "text")
    return FactSheet.model_validate_json(raw)


def extract_facts(source: Source, text: str) -> FactSheet:
    chunks = split_text(text)
    facts = []
    for i, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"  {source.id}: chunk {i}/{len(chunks)} ({len(chunk)} chars)")
        facts += _facts_call(source, chunk).facts
    sheet = FactSheet(source_id=source.id, facts=facts)  # never trust the model with the id
    for i, f in enumerate(sheet.facts, 1):
        f.id = f"{source.id}:F{i}"
    return sheet


# --------------------------------------------------------------------------------------
# Quote verification
# --------------------------------------------------------------------------------------

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def verify_facts(sheet: FactSheet, text: str) -> tuple[list[Fact], list[Fact]]:
    """Split facts into (verified, rejected). A quote is verified if it appears verbatim in the
    whitespace/punctuation-normalised source text. Ellipses split the quote into fragments that
    must each appear, in order."""
    hay = _norm(text)
    ok, bad = [], []
    for f in sheet.facts:
        fragments = [frag for frag in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", _norm(f.quote)) if frag]
        pos, good = 0, bool(fragments)
        for frag in fragments:
            i = hay.find(frag, pos)
            if i < 0:
                good = False
                break
            pos = i + len(frag)
        (ok if good else bad).append(f)
    return ok, bad


# --------------------------------------------------------------------------------------
# Pass B: synthesis
# --------------------------------------------------------------------------------------

LLM_FILLED_BY_CODE = {"provenance", "grounding", "validated", "sources"}


def map_schema_for_prompt() -> str:
    """ProcessMap JSON Schema minus the fields code fills in. The full schema is too large for the
    API's constrained decoding, so Pass B asks for JSON in the prompt and validates in code."""
    schema = ProcessMap.model_json_schema()
    for d in list(schema.get("$defs", {}).values()) + [schema]:
        for f in list(d.get("properties", {})):
            if f in LLM_FILLED_BY_CODE:
                d["properties"].pop(f)
                if f in d.get("required", []):
                    d["required"].remove(f)
    return json.dumps(schema, ensure_ascii=False)


def _json_only(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text.strip()


def synthesise(service_cfg: dict, sources: list[Source], facts: list[Fact]) -> ProcessMap:
    prompt = (PROMPTS / "synthesis.md").read_text()
    fact_lines = "\n".join(
        f"- {f.id} [{f.kind}] {f.statement}  «{f.quote[:220]}{'…' if len(f.quote) > 220 else ''}» ({f.locator})"
        for f in facts
    )
    source_lines = "\n".join(f"- {s.id}: {s.title} — {s.publisher}, layer={s.layer}, {s.language}" for s in sources)
    user = prompt.format(
        service_name=service_cfg["service_name"], country=service_cfg["country"],
        authority=service_cfg["authority"], sources=source_lines, facts=fact_lines,
    )
    user += ("\n\nOutput: return ONLY a JSON object (no prose, no code fence) that conforms to this JSON Schema. "
             "Omit nothing that is required.\n" + map_schema_for_prompt())
    messages = [{"role": "user", "content": user}]
    for attempt in range(2):
        with client.messages.stream(
            model=MODEL, max_tokens=128000, output_config={"effort": "high"}, messages=messages,
        ) as stream:
            msg = stream.get_final_message()
        if msg.stop_reason == "refusal":
            raise RuntimeError("refusal in synthesis")
        if msg.stop_reason == "max_tokens":
            raise RuntimeError("synthesis output hit max_tokens")
        raw = _json_only(next(b.text for b in msg.content if b.type == "text"))
        try:
            return ProcessMap.model_validate_json(raw)
        except Exception as e:  # one repair round with the validator's message
            if attempt == 1:
                (ROOT / "maps" / service_cfg["service_id"] / "map_invalid.json").write_text(raw)
                raise
            print(f"  synthesis JSON invalid, asking for a repair: {str(e)[:300]}")
            messages += [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"Your JSON failed validation:\n{str(e)[:4000]}\n\nReturn the complete corrected JSON object only."},
            ]


def attach_provenance(pm: ProcessMap, facts: list[Fact], sources: list[Source]) -> ProcessMap:
    by_id = {f.id: f for f in facts}
    src_of = {f.id: f.id.split(":")[0] for f in facts}

    def to_provenance(ids: list[str]) -> list[Passage]:
        out = []
        for fid in ids:
            f = by_id.get(fid)
            if f:
                out.append(Passage(source_id=src_of[fid], locator=f.locator, quote=f.quote, verified=True))
        return out

    for coll in (pm.nodes, pm.edges, pm.rules, pm.data_sources):
        for item in coll:
            item.provenance = to_provenance(item.provenance_fact_ids)
            item.grounding = "documented" if item.provenance else "inferred"
    pm.sources = sources
    return pm


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------

def run(service_dir: Path, stage: str = "all") -> None:
    import yaml

    cfg = yaml.safe_load((service_dir / "sources.yaml").read_text())
    service_id = cfg["service_id"]
    corpus_dir = ROOT / "corpus" / service_id
    out_dir = ROOT / "maps" / service_id
    out_dir.mkdir(parents=True, exist_ok=True)
    sheets_dir = out_dir / "facts"
    sheets_dir.mkdir(exist_ok=True)

    manifest = json.loads((corpus_dir / "manifest.json").read_text())
    sources = [Source(**s) for s in manifest["sources"]]
    texts = {s.id: (corpus_dir / f"{s.id}.txt").read_text() for s in sources}

    # Pass A, in parallel; each source's sheet is saved on its own so a failure loses only that source
    def facts_for(s: Source) -> FactSheet:
        p = sheets_dir / f"{s.id}.json"
        if p.exists():
            return FactSheet.model_validate_json(p.read_text())
        sheet = extract_facts(s, texts[s.id])
        p.write_text(sheet.model_dump_json(indent=2))
        return sheet

    todo = [s for s in sources if not (sheets_dir / f"{s.id}.json").exists()]
    print(f"Pass A: {len(sources) - len(todo)} sources cached, extracting {len(todo)} with {MODEL} …")
    with ThreadPoolExecutor(max_workers=max(1, len(sources))) as pool:
        sheets = list(pool.map(facts_for, sources))
    (out_dir / "facts.json").write_text(json.dumps({"sheets": [s.model_dump() for s in sheets]}, ensure_ascii=False, indent=2))

    verified, rejected, per_source = [], [], {}
    for sheet in sheets:
        ok, bad = verify_facts(sheet, texts[sheet.source_id])
        verified += ok
        rejected += bad
        per_source[sheet.source_id] = {"facts": len(sheet.facts), "verified": len(ok), "rejected": len(bad)}
        print(f"  {sheet.source_id}: {len(sheet.facts)} facts, {len(ok)} quotes verified, {len(bad)} rejected")
    (out_dir / "facts_rejected.json").write_text(json.dumps([f.model_dump() for f in rejected], ensure_ascii=False, indent=2))
    if stage == "facts":
        print(f"\nStopped after Pass A ({len(verified)} verified facts). Re-run with --stage map to synthesise.")
        return

    # Pass B
    print(f"Pass B: synthesising map from {len(verified)} verified facts …")
    pm = synthesise(cfg, sources, verified)
    pm = attach_provenance(pm, verified, sources)
    (out_dir / "map.json").write_text(pm.model_dump_json(indent=2))

    # Report
    nodes = pm.nodes
    report = {
        "service_id": service_id,
        "model": MODEL,
        "sources": per_source,
        "facts_total": sum(len(s.facts) for s in sheets),
        "facts_verified": len(verified),
        "facts_used_in_map": len({fid for coll in (pm.nodes, pm.edges, pm.rules, pm.data_sources) for item in coll for fid in item.provenance_fact_ids}),
        "nodes": len(nodes),
        "edges": len(pm.edges),
        "rules": len(pm.rules),
        "data_sources": len(pm.data_sources),
        "nodes_by_grounding": _count(n.grounding for n in nodes),
        "nodes_by_visibility": _count(n.visibility for n in nodes),
        "grounding_by_visibility": {
            v: _count(n.grounding for n in nodes if n.visibility == v) for v in ("external", "internal")
        },
        "nodes_by_automation_class": _count(n.automation_class for n in nodes),
        "nodes_by_agent_mode": _count(n.agent_mode for n in nodes),
        "nodes_by_actor": _count(n.actor_id for n in nodes),
        "rules_by_grounding": _count(r.grounding for r in pm.rules),
        "open_questions": len(pm.open_questions),
    }
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_dir / 'map.json'}")


def _count(items) -> dict:
    out: dict = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    stage_arg = sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "all"
    run(Path(sys.argv[1]).resolve(), stage=stage_arg)
