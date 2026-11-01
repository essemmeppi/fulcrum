"""python -m twin.cli <command>   (run from process-mapper/)

  limits                 check the formula against Kela's published income limits
  grid [out_dir]         run the synthetic grid, write runs and a summary
  oracle <results.json>  compare the twin with recorded Kela calculator results
  replay <dir>           run replayed published decisions and report divergence
  shadow <intake> <out>  shadow mode over a directory of mirrored cases
  case <file.json>       run one case and print the trace
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .case import Case, Expected
from .compare import compare
from .params import PARAMS_2026
from .rules import gha
from .runner import Runner
from .shadow import report, run_dir
from .synthetic import grid, make_case

KELA_LIMITS = {
    1: {(1, 0): 1844, (1, 1): 2630, (1, 2): 3348, (1, 3): 3982, (1, 4): 4574, (2, 0): 2428, (2, 1): 3146, (2, 2): 3780, (2, 3): 4372, (3, 0): 2944, (3, 1): 3578, (3, 2): 4170},
    3: {(1, 0): 1612, (1, 1): 2318, (1, 2): 2966, (1, 3): 3568, (1, 4): 4132, (2, 0): 2116, (2, 1): 2764, (2, 2): 3366, (2, 3): 3930, (3, 0): 2562, (3, 1): 3164, (3, 2): 3728},
    4: {(1, 0): 1506, (1, 1): 2162, (1, 2): 2778, (1, 3): 3356, (1, 4): 3910, (2, 0): 1960, (2, 1): 2576, (2, 2): 3154, (2, 3): 3708, (3, 0): 2374, (3, 1): 2952, (3, 2): 3506},
}


def cmd_limits() -> int:
    bad = 0
    for g, t in KELA_LIMITS.items():
        for (a, c), v in t.items():
            mine = gha.income_limit(a, c, g, PARAMS_2026)
            if mine != v:
                bad += 1
                print(f"MISMATCH group {g} {a}+{c}: kela {v} twin {mine}")
    n = sum(len(t) for t in KELA_LIMITS.values())
    print(f"income limits: {n - bad} of {n} reproduced")
    return 0 if not bad else 1


def cmd_grid(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    r = Runner()
    rows = []
    for case in grid():
        run = r.run(case)
        (out / f"{case.case_id}.run.json").write_text(run.to_json())
        rows.append({"case_id": case.case_id, "adults": case.adults, "children": case.children, "municipality": case.dwelling.municipality,
                     "rent": case.costs.rent, "income": sum(i.gross_monthly for m in case.members for i in m.incomes),
                     "decision": run.outcome.decision, "amount": run.outcome.monthly_allowance, "questions": run.outcome.open_questions, "grounds": run.outcome.grounds})
    (out / "summary.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    from collections import Counter
    print(Counter(x["decision"] for x in rows))
    return 0


def cmd_oracle(path: Path, out: Path) -> int:
    recs = json.loads(path.read_text())
    r = Runner()
    results = []
    for rec in recs:
        incomes = rec.get("incomes", [])
        ex = rec.get("extras", {})
        # The calculator expects the user to subtract the 2,000 EUR per-person deposit disregard before entering deposits;
        # the twin applies the disregard itself, so the entered figure is restored to a gross deposit here.
        deposits = float(ex.get("bank_deposits_eur_entered", 0) or 0)
        if deposits:
            deposits += PARAMS_2026.asset_deposit_reserve
        case = make_case(rec["id"], rec["adults"], rec["children"], rec["municipality"], rec["rent"], incomes,
                         water=bool(ex.get("water_paid_separately")), heating=bool(ex.get("heating_paid_separately")), deposits=deposits)
        if ex.get("electricity_paid_separately") is False and ex.get("floor_area_m2_entered"):
            case.costs.floor_area_m2 = float(ex["floor_area_m2_entered"])
        case.source.kind = "oracle"; case.source.url = rec.get("calculator_url", "")
        amt = rec.get("result_monthly_allowance")
        case.expected = Expected(outcome="granted" if amt else "rejected", monthly_allowance=float(amt or 0), decided_by="Kela calculator", reason=rec.get("result_text", "")[:200])
        run = r.run(case)
        results.append((case, compare(case, run)))
    out.mkdir(parents=True, exist_ok=True)
    (out / "oracle-report.md").write_text(report(results, "Stage 1: twin versus Kela calculator"))
    print(report(results, "Stage 1: twin versus Kela calculator"))
    return 0


def cmd_replay(d: Path, out: Path) -> int:
    results = run_dir(d, out)
    txt = report(results, "Stage 3: twin versus published appeal decisions")
    (out / "replay-report.md").write_text(txt)
    print(txt)
    return 0


def cmd_shadow(intake: Path, out: Path) -> int:
    results = run_dir(intake, out)
    txt = report(results, "Shadow run: twin versus real decisions")
    (out / "shadow-report.md").write_text(txt)
    print(txt)
    return 0


def cmd_case(f: Path) -> int:
    case = Case.model_validate(json.loads(f.read_text()))
    run = Runner().run(case)
    print(run.to_json())
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__); return 2
    cmd, args = argv[0], argv[1:]
    root = Path(__file__).resolve().parent
    if cmd == "limits": return cmd_limits()
    if cmd == "grid": return cmd_grid(Path(args[0]) if args else root / "runs" / "grid")
    if cmd == "oracle": return cmd_oracle(Path(args[0]), Path(args[1]) if len(args) > 1 else root / "runs" / "oracle")
    if cmd == "replay": return cmd_replay(Path(args[0]) if args else root / "cases" / "replay", Path(args[1]) if len(args) > 1 else root / "runs" / "replay")
    if cmd == "shadow": return cmd_shadow(Path(args[0]), Path(args[1]))
    if cmd == "case": return cmd_case(Path(args[0]))
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
