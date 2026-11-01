"""Synthetic case grid covering the rule branches of the calculation."""

from __future__ import annotations

import itertools

from .case import Assets, Case, Costs, Dwelling, Expected, Flags, Income, Member, SourceRef


def make_case(cid: str, adults: int, children: int, municipality: str, rent: float, incomes: list[float],
              water: bool = False, heating: bool = False, deposits: float = 0.0, date: str = "2026-10-01", **kw) -> Case:
    members = []
    for i in range(adults):
        role = "applicant" if i == 0 else ("spouse" if i == 1 else "other_adult")
        inc = [Income(kind="wage", gross_monthly=incomes[i])] if i < len(incomes) and incomes[i] else []
        members.append(Member(id=f"a{i+1}", role=role, age=35, incomes=inc, assets=Assets(deposits=deposits if i == 0 else 0.0)))
    for j in range(children):
        members.append(Member(id=f"c{j+1}", role="child", age=8))
    return Case(case_id=cid, source=SourceRef(kind="synthetic"), decision_date=date,
                dwelling=Dwelling(municipality=municipality), members=members,
                costs=Costs(rent=rent, water_paid_separately=water, heating_paid_separately=heating), flags=Flags(**kw))


def grid() -> list[Case]:
    cases = []
    n = 0
    for (adults, children), muni, rent, inc in itertools.product(
            [(1, 0), (1, 1), (2, 0), (2, 2), (3, 1)], ["Helsinki", "Turku", "Pori", "Rovaniemi", "Mariehamn"],
            [350, 600, 900, 1400], [0, 900, 1600, 2600]):
        n += 1
        per = [inc] + [0] * (adults - 1)
        cases.append(make_case(f"syn-{n:03d}", adults, children, muni, rent, per))
    # branch cases
    n += 1; cases.append(make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [1200], water=True))
    n += 1; cases.append(make_case(f"syn-{n:03d}", 2, 1, "Kuopio", 800, [1000, 800], heating=True))
    n += 1; cases.append(make_case(f"syn-{n:03d}", 1, 0, "Rovaniemi", 500, [1100], heating=True))
    n += 1; cases.append(make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [1200], deposits=25000))
    n += 1; cases.append(make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [1200], deposits=60000))
    n += 1; cases.append(make_case(f"syn-{n:03d}", 2, 2, "Helsinki", 1300, [1800, 1000], disabled_member_extra_space=True))
    n += 1; c = make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [0]); c.members[0].excluded_student = True; cases.append(c)
    n += 1; c = make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [0]); c.members[0].receives_excluding_pension = True; cases.append(c)
    n += 1; c = make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [0]); c.dwelling.tenure = "owner_occupied"; cases.append(c)
    n += 1; c = make_case(f"syn-{n:03d}", 1, 0, "Helsinki", 700, [1200]); c.unknowns = ["costs.rent not stated"]; c.costs.rent = 0; cases.append(c)
    return cases
