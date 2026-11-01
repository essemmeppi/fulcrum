"""Case model for the general housing allowance twin.

A case is everything the law needs to decide the service: the household, the dwelling,
the housing costs, the incomes and assets, and the date the decision applies from.
It is built from the map's data objects (process-mapper/maps/.../map.json) and is the
only input the runner accepts, whether the case is synthetic, replayed from a published
decision, mirrored from a live intake, or sent to an external oracle.

Unknown facts are allowed and are listed in `unknowns`; the runner treats a step whose
inputs are unknown as a question for a human, never as a guess.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Tenure = Literal["rental", "right_of_occupancy", "part_ownership", "owner_occupied"]
Region = Literal["default", "east", "north"]  # heating flat-rate regions (R_CALC_WATER_HEATING_FLAT)
MemberRole = Literal["applicant", "spouse", "child", "parent", "other_adult", "other_child"]
IncomeKind = Literal[
    "wage", "entrepreneur", "benefit", "unemployment", "pension", "study_grant",
    "capital", "rental", "interest_dividend", "child_benefit", "maintenance", "other_privileged", "other",
]
CaseKind = Literal["synthetic", "oracle", "replay", "shadow"]


class Income(BaseModel):
    kind: IncomeKind
    gross_monthly: float = Field(ge=0)
    continuous: bool = True
    note: str = ""


class Assets(BaseModel):
    deposits: float = 0.0
    other: float = 0.0            # shares, funds, real estate etc. (R_CALC_ASSETS_AS_INCOME)
    long_term_debts: float = 0.0


class Member(BaseModel):
    id: str
    role: MemberRole
    age: Optional[int] = None
    resident_in_finland: Optional[bool] = True
    excluded_student: bool = False            # § 4(4): a student who came to Finland to study
    receives_excluding_pension: bool = False  # R_ELIG_PENSIONER_EXCLUSION
    incomes: list[Income] = []
    assets: Assets = Assets()


class Dwelling(BaseModel):
    municipality: str = ""
    municipality_group: Optional[Literal[1, 2, 3, 4]] = None
    region: Region = "default"
    tenure: Tenure = "rental"
    in_finland: bool = True
    aland: bool = False


class Costs(BaseModel):
    rent: float = Field(0.0, ge=0, description="Monthly rent or usage charge paid by household members")
    water_paid_separately: bool = False
    heating_paid_separately: bool = False
    electricity_included_in_rent: float = 0.0  # deducted from rent (R_CALC_ACCEPTED_COSTS)
    excluded_fees_in_rent: float = 0.0         # sauna, parking, internet etc. included in the figure above
    subtenant_rent: float = 0.0                # R_CALC_SUBTENANT_DEDUCTION
    employer_paid_share: float = 0.0


class Flags(BaseModel):
    disabled_member_extra_space: bool = False  # R_CALC_DISABILITY_SPACE
    excluded_student_in_dwelling: int = 0      # R_CALC_STUDENT_SHARE: number of excluded students sharing


class Expected(BaseModel):
    """What the real system decided, when known. The twin is compared against this."""
    outcome: Optional[Literal["granted", "rejected", "revised", "terminated", "recovery", "unknown"]] = None
    monthly_allowance: Optional[float] = None
    reason: str = ""
    decided_by: str = ""  # e.g. "Kela calculator", "SAMU 2023/123", "Insurance Court"


class SourceRef(BaseModel):
    kind: CaseKind
    url: str = ""
    citation: str = ""
    quotes: list[str] = []
    fetched_at: str = ""


class Case(BaseModel):
    case_id: str
    source: SourceRef
    decision_date: str = Field(description="ISO date the decision applies from; selects the parameter set")
    dwelling: Dwelling
    members: list[Member]
    costs: Costs
    flags: Flags = Flags()
    expected: Expected = Expected()
    unknowns: list[str] = []
    notes: str = ""

    @property
    def adults(self) -> int:
        return sum(1 for m in self.members if m.role in ("applicant", "spouse", "parent", "other_adult"))

    @property
    def children(self) -> int:
        return sum(1 for m in self.members if m.role in ("child", "other_child"))
