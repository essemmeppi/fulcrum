"""Rules as code for the general housing allowance. One function per rule family of the map.

Every function returns a Result: a value plus the rule ids it applied and a one-line explanation
per applied rule, so the runner can write a trace that cites the map (and through the map, the law).
Nothing here guesses: when a fact the rule needs is unknown, the function raises Unknown and the
runner turns that into a question for a human.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..case import Case, Member
from ..params import ALAND, GROUP_1, GROUP_3, REGION_EAST, REGION_NORTH, ParamSet


class Unknown(Exception):
    """A fact the rule needs is not in the case."""


@dataclass
class Result:
    value: Any
    applied: list[tuple[str, str]] = field(default_factory=list)  # (rule_id, explanation)

    def note(self, rule_id: str, text: str) -> None:
        self.applied.append((rule_id, text))


def r2(x: float) -> float:
    return round(x + 1e-9, 2)


# --- Dwelling -----------------------------------------------------------------------------

def municipality_group(case: Case, p: ParamSet | None = None) -> Result:
    d = case.dwelling
    if d.municipality_group is not None:
        g = d.municipality_group
        if p is not None and g not in p.max_costs:
            g = 1 if g == 2 else g
        return Result(g, [("R_CALC_MAX_COSTS", f"municipality group given as {d.municipality_group}")])
    name = d.municipality.strip().lower()
    if not name:
        raise Unknown("dwelling.municipality")
    if d.aland or name in ALAND:
        g = 0
    elif name in GROUP_1:
        g = 2 if (p is not None and 2 in p.max_costs and name != "helsinki") else 1
    elif name in GROUP_3:
        g = 3
    else:
        g = 4
    return Result(g, [("R_CALC_MAX_COSTS", f"{d.municipality} is in municipality group {g or 'Åland'}")])


def region(case: Case) -> str:
    if case.dwelling.region != "default":
        return case.dwelling.region
    name = case.dwelling.municipality.strip().lower()
    if name in REGION_EAST:
        return "east"
    if name in REGION_NORTH:
        return "north"
    return "default"


# --- Household ----------------------------------------------------------------------------

def household(case: Case) -> Result:
    """Counts adults and children; applies the always-same-household rule as the case states it."""
    adults, children = case.adults, case.children
    res = Result((max(adults, 1), children))
    res.note("R_HH_DEFINITION", f"household of {adults} adult(s) and {children} child(ren)")
    if adults == 0:
        res.note("R_CALC_BASIC_DEDUCTIBLE", "no adult listed; at least one adult is always assumed")
    return res


# --- Costs ----------------------------------------------------------------------------------

def accepted_costs(case: Case, p: ParamSet) -> Result:
    c, d = case.costs, case.dwelling
    size = case.adults + case.children
    if d.tenure == "owner_occupied" and not p.owner_occupied_covered:
        res = Result(0.0)
        res.note("R_CALC_ACCEPTED_COSTS", "owner-occupied home: no housing costs accepted under current guidance")
        return res
    if d.tenure == "owner_occupied":
        raise Unknown("owner-occupier maintenance and financing costs (§ 9) are not encoded")
    if c.rent <= 0 and not case.unknowns:
        raise Unknown("costs.rent")
    if "costs.rent not stated" in case.unknowns or (c.rent <= 0):
        raise Unknown("costs.rent")
    base = c.rent - c.electricity_included_in_rent - c.excluded_fees_in_rent - c.employer_paid_share - c.subtenant_rent
    res = Result(0.0)
    res.note("R_CALC_ACCEPTED_COSTS", f"rent {c.rent:.2f} minus electricity {c.electricity_included_in_rent:.2f}, excluded fees {c.excluded_fees_in_rent:.2f}, employer share {c.employer_paid_share:.2f}")
    if c.subtenant_rent:
        res.note("R_CALC_SUBTENANT_DEDUCTION", f"subtenant rent {c.subtenant_rent:.2f} deducted")
    extras = 0.0
    if c.water_paid_separately:
        extras += p.water_per_person * size
        res.note("R_CALC_WATER_HEATING_FLAT", f"water {p.water_per_person} x {size} persons = {p.water_per_person*size}")
    if c.heating_paid_separately:
        first, each = p.heating[region(case)]
        h = first + each * max(size - 1, 0)
        extras += h
        res.note("R_CALC_WATER_HEATING_FLAT", f"heating {first} + {each} x {max(size-1,0)} = {h} (region {region(case)})")
    total = max(base, 0.0) + extras
    if case.flags.excluded_student_in_dwelling:
        n = case.flags.excluded_student_in_dwelling
        share = size / (size + n)
        total = total * share
        res.note("R_CALC_STUDENT_SHARE", f"{n} excluded student(s) share the dwelling: costs x {size}/{size+n}")
    res.value = r2(total)
    return res


def max_costs(case: Case, p: ParamSet) -> Result:
    g = municipality_group(case, p)
    size = case.adults + case.children
    res = Result(0.0, list(g.applied))
    if case.flags.disabled_member_extra_space:
        size += 1
        res.note("R_CALC_DISABILITY_SPACE", "disabled member with large space needs: table size + 1")
    table = p.max_costs_aland if g.value == 0 else p.max_costs[g.value]
    if size <= 4:
        v = table[size - 1]
    else:
        v = table[3] + table[4] * (size - 4)
    res.value = float(v)
    res.note("R_CALC_MAX_COSTS", f"maximum housing costs for {size} person(s) in group {g.value or 'Åland'}: {v}")
    return res


# --- Income ---------------------------------------------------------------------------------

PRIVILEGED = {"child_benefit", "maintenance", "other_privileged"}


def member_income(m: Member, p: ParamSet, res: Result) -> float:
    total = 0.0
    earned = 0.0
    for inc in m.incomes:
        if inc.kind in PRIVILEGED:
            res.note("R_CALC_PRIVILEGED_INCOME", f"{m.id}: {inc.kind} {inc.gross_monthly:.2f} not counted")
            continue
        if inc.kind == "interest_dividend":
            if inc.gross_monthly <= p.interest_dividend_threshold:
                res.note("R_CALC_INTEREST_DIVIDEND_THRESHOLD", f"{m.id}: interest/dividend {inc.gross_monthly:.2f} at or below {p.interest_dividend_threshold}, not counted")
                continue
        if inc.kind in ("wage", "entrepreneur"):
            earned += inc.gross_monthly
        total += inc.gross_monthly
        res.note("R_CALC_INCOME_DEFINITION", f"{m.id}: {inc.kind} {inc.gross_monthly:.2f}{'' if inc.continuous else ' (averaged)'}")
    if p.earned_income_deduction and earned:
        d = min(p.earned_income_deduction, earned)
        total -= d
        res.note("R_CALC_EARNED_INCOME_DEDUCTION", f"{m.id}: earned income deduction {d:.2f}")
    return total


def asset_income(case: Case, p: ParamSet) -> Result:
    res = Result(0.0)
    adults = max(case.adults, 1)
    net = 0.0
    for m in case.members:
        if m.role in ("child", "other_child"):
            continue
        dep = max(m.assets.deposits - p.asset_deposit_reserve, 0.0)
        net += dep + m.assets.other - m.assets.long_term_debts
    net = max(net, 0.0)
    threshold = p.asset_threshold_one_adult if adults == 1 else p.asset_threshold_two_adults
    res.note("R_CALC_ASSETS_AS_INCOME", f"net counted assets {net:.2f} (deposits less {p.asset_deposit_reserve} per member, less long-term debts); threshold {threshold}")
    if net >= p.asset_ceiling:
        res.note("R_ELIG_ASSET_LIMIT", f"assets {net:.2f} at or above {p.asset_ceiling}: no allowance")
        res.value = ("ceiling", net)
        return res
    excess = max(net - threshold, 0.0)
    monthly = r2(excess * p.asset_income_share / 12)
    if excess:
        res.note("R_CALC_ASSETS_AS_INCOME", f"{p.asset_income_share:.0%} of excess {excess:.2f} per year = {monthly:.2f} per month")
    res.value = ("income", monthly)
    return res


def household_income(case: Case, p: ParamSet) -> Result:
    res = Result(0.0)
    total = 0.0
    for m in case.members:
        if m.role in ("child", "other_child") and m.age is not None and m.age < 18:
            if m.incomes:
                res.note("R_CALC_INCOME_DEFINITION", f"{m.id}: minor's income not counted")
            continue
        total += member_income(m, p, res)
    a = asset_income(case, p)
    res.applied += a.applied
    if a.value[0] == "income":
        total += a.value[1]
    res.value = r2(total)
    res.note("R_CALC_ROUNDING", f"combined household income {total:.2f}, rounded to full euros {round(total)}")
    return res


# --- Deductible and amount ------------------------------------------------------------------

def basic_deductible(case: Case, p: ParamSet, income: float) -> Result:
    adults, children = household(case).value
    T = round(income)
    if municipality_group(case).value == 0:
        share, base, pa, pc = p.deductible_share_aland, p.deductible_base_aland, p.deductible_per_adult_aland, p.deductible_per_child_aland
    else:
        share, base, pa, pc = p.deductible_share, p.deductible_base, p.deductible_per_adult, p.deductible_per_child
    raw = share * (T - (base + pa * adults + pc * children))
    res = Result(0.0)
    res.note("R_CALC_BASIC_DEDUCTIBLE", f"{share} x [{T} - ({base} + {pa} x {adults} + {pc} x {children})] = {raw:.2f}")
    if raw < p.min_deductible:
        res.note("R_CALC_BASIC_DEDUCTIBLE", f"deductible {raw:.2f} below {p.min_deductible}: disregarded")
        res.value = 0.0
    else:
        res.value = r2(raw)
    return res


def allowance(case: Case, p: ParamSet, costs: float, cap: float, deductible: float) -> Result:
    rate = p.rate_aland if municipality_group(case).value == 0 else p.rate
    counted = min(costs, cap)
    amount = r2(rate * (counted - deductible))
    res = Result(max(amount, 0.0))
    res.note("R_CALC_FORMULA", f"{rate} x (min({costs:.2f}, {cap:.0f}) - {deductible:.2f}) = {amount:.2f}")
    if amount < p.min_payment:
        res.note("R_CALC_MIN_PAYMENT", f"{amount:.2f} below {p.min_payment}: not paid")
        res.value = 0.0
    return res


# --- Eligibility gates ---------------------------------------------------------------------

def eligibility(case: Case, p: ParamSet) -> Result:
    """Conditions a caseworker checks before the calculation. Value: list of failed condition ids."""
    failed: list[str] = []
    res = Result(failed)
    d = case.dwelling
    if not d.in_finland:
        failed.append("R_ELIG_DWELLING"); res.note("R_ELIG_DWELLING", "dwelling not in Finland")
    if d.tenure == "owner_occupied" and not p.owner_occupied_covered:
        failed.append("R_ELIG_DWELLING"); res.note("R_ELIG_DWELLING", "owner-occupied home not covered")
    for m in case.members:
        if m.resident_in_finland is None:
            raise Unknown(f"members[{m.id}].resident_in_finland")
        if not m.resident_in_finland:
            failed.append("R_ELIG_RESIDENCE"); res.note("R_ELIG_RESIDENCE", f"{m.id} not permanently resident in Finland")
        if m.excluded_student and m.role == "applicant" and p.students_excluded_by_default:
            failed.append("R_ELIG_STUDENT"); res.note("R_ELIG_STUDENT", f"{m.id} is a student: study grant housing supplement applies instead")
        if m.receives_excluding_pension and case.adults == 1:
            failed.append("R_ELIG_PENSIONER_EXCLUSION"); res.note("R_ELIG_PENSIONER_EXCLUSION", f"{m.id} receives a pension that entitles to the pensioners' housing allowance")
    if not failed:
        res.note("R_ELIG_DWELLING", "dwelling and tenure eligible"); res.note("R_ELIG_RESIDENCE", "all members resident in Finland")
    return res


def income_limit(adults: int, children: int, group: int, p: ParamSet, disabled_extra: bool = False) -> int:
    """Highest integer income at which the allowance is still at least the minimum payment.
    Kela publishes these as 'income limits'; they follow from the formula, so they are a check on it."""
    size = adults + children + (1 if disabled_extra else 0)
    table = p.max_costs_aland if group == 0 else p.max_costs[group]
    cap = table[size - 1] if size <= 4 else table[3] + table[4] * (size - 4)
    rate = p.rate_aland if group == 0 else p.rate
    if group == 0:
        share, base, pa, pc = p.deductible_share_aland, p.deductible_base_aland, p.deductible_per_adult_aland, p.deductible_per_child_aland
    else:
        share, base, pa, pc = p.deductible_share, p.deductible_base, p.deductible_per_adult, p.deductible_per_child
    # rate * (cap - share*(T - K)) >= min_payment  =>  T <= K + (cap - min_payment/rate)/share
    K = base + pa * adults + pc * children
    T = K + (cap - p.min_payment / rate) / share
    return int(T)
