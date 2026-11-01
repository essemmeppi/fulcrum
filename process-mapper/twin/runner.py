"""Walks the process map as a state machine and writes a trace per step.

Who executes a node follows its automation class in the map:
  deterministic_rule  -> a rule function (rules/gha.py)
  register_lookup     -> a registry adapter
  document_check,
  judgment            -> a Judge: scripted from the case by default; an LLM judge can be plugged in
  human_signoff       -> a gate: the run emits a proposal and stops for a person
  notification        -> a drafted message
  citizen_action      -> taken from the case (the case is the application)
Edges are followed by matching the condition label a decision handler returns.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from .adapters import FixtureRegistry, Registry
from .case import Case
from .params import ParamSet, params_for
from .rules import gha
from .rules.gha import Result, Unknown

MAP_PATH = Path(__file__).resolve().parents[1] / "maps" / "fi-kela-general-housing-allowance" / "map.json"


@dataclass
class Step:
    node_id: str
    name: str
    actor: str
    automation_class: str
    agent_mode: str
    executed_by: str            # rule | registry | judge | gate | draft | case | skipped
    status: str                 # done | proposal | question | skipped
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    rules_applied: list[dict] = field(default_factory=list)
    provenance: list[dict] = field(default_factory=list)
    chosen_edge: Optional[str] = None
    question: Optional[str] = None


@dataclass
class Outcome:
    decision: str               # granted | rejected | not_paid | question
    monthly_allowance: float = 0.0
    grounds: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    proposals: list[str] = field(default_factory=list)


@dataclass
class Run:
    case_id: str
    started_at: str
    params_valid_from: str
    steps: list[Step]
    outcome: Outcome
    state: dict

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


class Judge:
    """Scripted judge: answers judgment and document-check nodes from the case's own facts.
    Replace with an LLM-backed judge (same signature) when a model key is available."""

    def __call__(self, node_id: str, case: Case, state: dict) -> Result:
        if node_id == "T_COMPLETENESS":
            missing = [u for u in case.unknowns]
            return Result({"complete": not missing, "missing": missing}, [("R_PROC_APPLICATION_CONTENT", "complete" if not missing else f"missing: {', '.join(missing)}")])
        if node_id == "D_COMPLETE":
            return Result("All information needed to decide is available" if state.get("complete", True) else "Application or attachments incomplete")
        if node_id == "D_INFO_PROVIDED":
            return Result("Applicant refuses or fails to provide information within reasonable time – decide on available information")
        if node_id == "T_RESIDENCE":
            unknown = [m.id for m in case.members if m.resident_in_finland is None]
            if unknown:
                raise Unknown(f"residence of {', '.join(unknown)}")
            return Result({m.id: m.resident_in_finland for m in case.members}, [("R_ELIG_RESIDENCE", "residence as stated in the case")])
        if node_id == "T_HOUSEHOLD":
            return gha.household(case)
        if node_id == "T_INCOME":
            return gha.household_income(case, state["params"])
        if node_id == "T_ELIG_CHECK":
            return gha.eligibility(case, state["params"])
        if node_id == "T_DECIDE":
            return Result("proposal")
        raise Unknown(f"no scripted answer for {node_id}")


class Runner:
    def __init__(self, map_path: Path = MAP_PATH, registry: Optional[Registry] = None, judge: Optional[Callable] = None):
        self.map = json.loads(Path(map_path).read_text())
        self.nodes = {n["id"]: n for n in self.map["nodes"]}
        self.edges: dict[str, list[dict]] = {}
        for e in self.map["edges"]:
            self.edges.setdefault(e["source"], []).append(e)
        self.rules = {r["id"]: r for r in self.map["rules"]}
        self.registry = registry or FixtureRegistry()
        self.judge = judge or Judge()

    # -- node handlers -------------------------------------------------------------------
    def handle(self, node: dict, case: Case, state: dict) -> tuple[Result, str, str]:
        """Returns (result, executed_by, status)."""
        nid, cls = node["id"], node["automation_class"]
        p: ParamSet = state["params"]
        if cls == "citizen_action":
            return Result({"from_case": True}), "case", "done"
        if cls == "register_lookup":
            fn = {"T_FETCH_INCOME": self.registry.incomes, "T_FETCH_LEASE": self.registry.lease, "T_FETCH_TAX": self.registry.taxation, "T_FETCH_OTHER": self.registry.dwelling_and_benefits}[nid]
            lr = fn(case)
            return Result({"source": lr.source_id, "found": lr.found, "data": lr.data, "note": lr.note}), "registry", "done"
        if cls in ("document_check", "judgment"):
            return self.judge(nid, case, state), "judge", "done"
        if cls == "human_signoff":
            return Result("proposal"), "gate", "proposal"
        if cls == "notification":
            return Result({"draft": self.draft(nid, case, state)}), "draft", "done"
        # deterministic_rule
        if nid == "T_REGISTER":
            return Result({"arrival_date": case.decision_date, "case_id": case.case_id}, [("R_DL_PROCESSING_TIME", "arrival date recorded")]), "rule", "done"
        if nid == "T_ASSETS":
            return gha.asset_income(case, p), "rule", "done"
        if nid == "T_COSTS":
            r = gha.accepted_costs(case, p); state["costs"] = r.value
            m = gha.max_costs(case, p); state["cap"] = m.value
            r.applied += m.applied; r.value = {"accepted_costs": r.value, "max_costs": m.value}
            return r, "rule", "done"
        if nid == "D_ELIGIBLE":
            failed = state.get("eligibility_failed", [])
            if state.get("asset_ceiling"):
                failed = failed + ["R_ELIG_ASSET_LIMIT"]
            label = "All eligibility conditions met" if not failed else "Any condition not met (income/asset limit exceeded, ineligible dwelling, student or pensioner exclusion, non-residence) – rejection or termination"
            state["eligibility_failed"] = failed
            return Result(label, [(f, "failed") for f in failed] or [("R_ELIG_DWELLING", "met")]), "rule", "done"
        if nid == "T_CALC":
            d = gha.basic_deductible(case, p, state["income"]); state["deductible"] = d.value
            a = gha.allowance(case, p, state["costs"], state["cap"], d.value); state["amount"] = a.value
            d.applied += a.applied; d.value = {"basic_deductible": d.value, "monthly_allowance": a.value}
            return d, "rule", "done"
        if nid == "D_MIN_AMOUNT":
            ok = state.get("amount", 0.0) >= p.min_payment
            return Result("Amount ≥ 15 €/month – grant" if ok else "Amount < 15 €/month – not paid", [("R_CALC_MIN_PAYMENT", f"amount {state.get('amount',0):.2f}")]), "rule", "done"
        if nid == "D_PAYABLE":
            ok = state.get("decision") == "granted"
            return Result("Allowance granted or continues in payment" if ok else "Rejected, below minimum or terminated"), "rule", "done"
        if nid == "E_NOT_PAYABLE":
            return Result("end"), "rule", "done"
        raise Unknown(f"no handler for {nid}")

    def draft(self, nid: str, case: Case, state: dict) -> str:
        if nid == "T_REQUEST_INFO":
            return "Request for additional information: " + "; ".join(state.get("missing", [])) + ". Please reply within the time limit; otherwise the matter is decided on the available information."
        if nid == "T_NOTIFY":
            if state.get("decision") == "granted":
                return f"Decision: general housing allowance granted, {state['amount']:.2f} EUR per month from {case.decision_date}. Accepted housing costs {state['costs']:.2f} (maximum {state['cap']:.0f}), household income {state['income']:.2f}, basic deductible {state['deductible']:.2f}."
            if state.get("decision") == "not_paid":
                return f"Decision: the calculated allowance {state['amount_raw']:.2f} EUR is below the minimum of 15 EUR per month and is not paid."
            return "Decision: application rejected. Grounds: " + ", ".join(state.get("eligibility_failed", []))
        return ""

    # -- the walk ------------------------------------------------------------------------
    def run(self, case: Case, stop_at: str = "D_PAYABLE", max_steps: int = 60) -> Run:
        p = params_for(case.decision_date)
        state: dict = {"params": p, "complete": not case.unknowns, "missing": list(case.unknowns)}
        steps: list[Step] = []
        outcome = Outcome("question")
        nid = "S_APPLY"
        seen_request = False
        for _ in range(max_steps):
            node = self.nodes[nid]
            step = Step(nid, node["name"], node["actor_id"], node["automation_class"], node["agent_mode"], "", "")
            try:
                res, by, status = self.handle(node, case, state)
                step.executed_by, step.status = by, status
                step.outputs = res.value if isinstance(res.value, dict) else {"value": res.value}
                step.rules_applied = [{"rule_id": r, "explanation": x} for r, x in res.applied]
                step.provenance = [{"rule_id": r, "source": pv.get("source_id"), "locator": pv.get("locator")} for r, _ in res.applied if r in self.rules for pv in self.rules[r].get("provenance", [])[:1]]
                # state updates from judged/ruled nodes
                if nid == "T_COMPLETENESS":
                    state["complete"], state["missing"] = res.value["complete"], res.value["missing"]
                if nid == "T_INCOME":
                    state["income"] = res.value
                if nid == "T_ASSETS" and res.value[0] == "ceiling":
                    state["asset_ceiling"] = True
                if nid == "T_ELIG_CHECK":
                    state["eligibility_failed"] = list(res.value)
                if nid == "D_ELIGIBLE" and state["eligibility_failed"]:
                    state["decision"] = "rejected"
                if nid == "D_MIN_AMOUNT":
                    state["amount_raw"] = state["amount"]
                    state["decision"] = "granted" if state["amount"] >= p.min_payment else "not_paid"
                if status == "proposal":
                    outcome.proposals.append(f"{nid}: {self.draft('T_NOTIFY', case, state)}")
            except Unknown as u:
                step.executed_by, step.status, step.question = "judge", "question", str(u)
                outcome.open_questions.append(f"{nid}: {u}")
                steps.append(step)
                break
            steps.append(step)
            if nid == stop_at:
                break
            # choose edge
            outs = self.edges.get(nid, [])
            if not outs:
                break
            if len(outs) == 1:
                nxt = outs[0]
            else:
                label = res.value if isinstance(res.value, str) else None
                nxt = next((e for e in outs if e.get("condition") == label), None)
                if nxt is None:
                    # D_COMPLETE after one info request: decide on available information
                    nxt = outs[0]
            step.chosen_edge = nxt.get("condition")
            if nid == "T_REQUEST_INFO":
                seen_request = True
            if nid == "D_INFO_PROVIDED" and seen_request:
                # scripted: no answer arrives in a replay; continue on available information
                pass
            nid = nxt["target"]
        if not outcome.open_questions:
            outcome.decision = state.get("decision", "question")
            outcome.monthly_allowance = state.get("amount", 0.0) if outcome.decision == "granted" else 0.0
            outcome.grounds = state.get("eligibility_failed", [])
        public_state = {k: v for k, v in state.items() if k != "params"}
        return Run(case.case_id, datetime.now(timezone.utc).isoformat(timespec="seconds"), p.valid_from, steps, outcome, public_state)
