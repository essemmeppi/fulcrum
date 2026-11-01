"""Shadow mode: run mirrored cases, never act, write a divergence report.

Intake: a directory of case JSON files (what a mirror of the real intake would write).
Outcomes: when the real decision arrives, it is added to the case's `expected` block and the case
is re-compared. The report is what a process owner reads each week.
Nothing in this module sends anything to a citizen, a register or a payment system.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .case import Case
from .compare import Verdict, compare
from .runner import Runner


def run_dir(intake: Path, out: Path, runner: Runner | None = None) -> list[tuple[Case, Verdict]]:
    runner = runner or Runner()
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for f in sorted(intake.glob("*.json")):
        case = Case.model_validate(json.loads(f.read_text()))
        run = runner.run(case)
        (out / f"{case.case_id}.run.json").write_text(run.to_json())
        results.append((case, compare(case, run)))
    return results


def report(results: list[tuple[Case, Verdict]], title: str) -> str:
    kinds = Counter(v.kind for _, v in results)
    lines = [f"# {title}", "", f"Cases: {len(results)}. Agree on amount: {kinds.get('agree',0)}. Agree on decision, amount not computable: {kinds.get('agree_decision',0)}. Amount differs: {kinds.get('amount',0)}. Decision differs: {kinds.get('decision',0)}. Twin asked a question: {kinds.get('twin_question',0)}. Untestable from the stated facts: {kinds.get('untestable',0)}. No real outcome yet: {kinds.get('no_expectation',0)}.", ""]
    lines += ["| case | twin | amount | real | kind | detail |", "|---|---|---|---|---|---|"]
    for c, v in results:
        lines.append(f"| {c.case_id} | {v.twin_decision} | {v.twin_amount:.2f} | {v.expected_outcome or ''} {'' if v.expected_amount is None else f'{v.expected_amount:.2f}'} | {v.kind} | {v.detail.replace('|','/')} |")
    qs = [(c.case_id, q) for c, v in results if v.kind == "twin_question" for q in [v.detail]]
    if qs:
        lines += ["", "## Questions the twin could not answer from the case", ""] + [f"- {cid}: {q}" for cid, q in qs]
    return "\n".join(lines) + "\n"
