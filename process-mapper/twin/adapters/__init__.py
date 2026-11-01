"""Register adapters. One interface per data source in the map; two implementations each.

FixtureRegistry answers from the case itself (synthetic, replay, oracle cases).
A real adapter (Incomes Register, DVV, landlord feeds, Kela's own records) implements the same
interface against the authority's API and is only ever read-only in shadow mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..case import Case


@dataclass
class LookupResult:
    source_id: str
    found: bool
    data: dict
    note: str = ""


class Registry(Protocol):
    def incomes(self, case: Case) -> LookupResult: ...
    def lease(self, case: Case) -> LookupResult: ...
    def taxation(self, case: Case) -> LookupResult: ...
    def dwelling_and_benefits(self, case: Case) -> LookupResult: ...


class FixtureRegistry:
    """Returns what the case states, marked as coming from the register the map names."""

    def incomes(self, case: Case) -> LookupResult:
        rows = [{"member": m.id, "kind": i.kind, "gross_monthly": i.gross_monthly} for m in case.members for i in m.incomes if i.kind in ("wage", "benefit", "unemployment", "pension")]
        return LookupResult("ds_incomes_register", bool(rows), {"rows": rows}, "fixture: incomes as stated in the case")

    def lease(self, case: Case) -> LookupResult:
        return LookupResult("ds_landlord_lease_service", case.costs.rent > 0, {"rent": case.costs.rent, "tenure": case.dwelling.tenure}, "fixture")

    def taxation(self, case: Case) -> LookupResult:
        rows = [{"member": m.id, "kind": i.kind, "gross_monthly": i.gross_monthly} for m in case.members for i in m.incomes if i.kind in ("entrepreneur", "capital", "rental", "interest_dividend")]
        return LookupResult("ds_tax_administration", bool(rows), {"rows": rows}, "fixture")

    def dwelling_and_benefits(self, case: Case) -> LookupResult:
        return LookupResult("ds_population_information_system", bool(case.dwelling.municipality), {"municipality": case.dwelling.municipality, "pensions": [m.id for m in case.members if m.receives_excluding_pension]}, "fixture")
