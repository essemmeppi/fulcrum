"""Compare a run with what the real system decided, and classify the divergence."""

from __future__ import annotations

from dataclasses import dataclass

from .case import Case
from .runner import Run

TOL = 0.01


@dataclass
class Verdict:
    case_id: str
    match: bool
    kind: str          # agree | amount | decision | twin_question | no_expectation
    detail: str
    twin_decision: str
    twin_amount: float
    expected_outcome: str | None
    expected_amount: float | None


def compare(case: Case, run: Run) -> Verdict:
    e = case.expected
    o = run.outcome
    if e.outcome is None and e.monthly_allowance is None:
        return Verdict(case.case_id, False, "no_expectation", "no real outcome recorded for this case", o.decision, o.monthly_allowance, None, None)
    if o.decision == "question":
        return Verdict(case.case_id, False, "twin_question", "; ".join(o.open_questions), o.decision, 0.0, e.outcome, e.monthly_allowance)
    exp_dec = {"granted": "granted", "rejected": "rejected", "terminated": "rejected", "revised": "granted"}.get(e.outcome or "", None)
    if e.monthly_allowance is not None:
        if e.monthly_allowance == 0 and o.decision in ("rejected", "not_paid"):
            return Verdict(case.case_id, True, "agree", "both: nothing payable", o.decision, 0.0, e.outcome, e.monthly_allowance)
        if abs(o.monthly_allowance - e.monthly_allowance) <= TOL:
            return Verdict(case.case_id, True, "agree", f"amount {o.monthly_allowance:.2f}", o.decision, o.monthly_allowance, e.outcome, e.monthly_allowance)
        return Verdict(case.case_id, False, "amount", f"twin {o.monthly_allowance:.2f} vs real {e.monthly_allowance:.2f} (diff {o.monthly_allowance - e.monthly_allowance:+.2f})", o.decision, o.monthly_allowance, e.outcome, e.monthly_allowance)
    if exp_dec is None:
        return Verdict(case.case_id, False, "no_expectation", f"expected outcome '{e.outcome}' is not a decision the application flow produces", o.decision, o.monthly_allowance, e.outcome, None)
    twin_dec = "granted" if o.decision == "granted" else "rejected"
    if twin_dec == exp_dec:
        return Verdict(case.case_id, True, "agree", f"decision {twin_dec}", o.decision, o.monthly_allowance, e.outcome, None)
    return Verdict(case.case_id, False, "decision", f"twin {o.decision} ({', '.join(o.grounds) or 'no ground'}) vs real {e.outcome}: {e.reason}", o.decision, o.monthly_allowance, e.outcome, None)
