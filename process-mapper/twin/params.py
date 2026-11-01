"""Dated parameter sets for the general housing allowance (Act 938/2014).

Every number carries its source. A case's `decision_date` selects the set in force.
Values observed on kela.fi on 2026-11-01 (page dated 12/10/2026). Where the consolidated Act
text (Finlex, 2010 index level) differs, the current guidance value is used and the Act value
is kept in `notes` so the conflict stays visible (R_CALC_INDEXATION).
"""

from __future__ import annotations

from dataclasses import dataclass, field

KELA_INCOME_PAGE = "https://www.kela.fi/housing-allowance-income-and-assets"
KELA_MAIN_PAGE = "https://www.kela.fi/general-housing-allowance"

# Municipality groups as published by Kela (Oct 2026). Groups I and II of the Act text are
# presented together on kela.fi ("Espoo, Helsinki, Kauniainen and Vantaa").
GROUP_1 = {"espoo", "helsinki", "kauniainen", "vantaa"}
GROUP_3 = {
    "hyvinkää", "hämeenlinna", "joensuu", "jyväskylä", "järvenpää", "kerava", "kirkkonummi", "kuopio",
    "lahti", "lohja", "nokia", "nurmijärvi", "oulu", "porvoo", "raisio", "riihimäki", "rovaniemi",
    "seinäjoki", "sipoo", "siuntio", "tampere", "turku", "tuusula", "vihti",
}
ALAND = {
    "brändö", "eckerö", "finström", "föglö", "geta", "hammarland", "jomala", "kumlinge", "kökar",
    "lemland", "lumparland", "maarianhamina", "mariehamn", "saltvik", "sottunga", "sund", "vårdö",
}
# Regions with higher heating flat rates (R_CALC_WATER_HEATING_FLAT); municipality -> region
REGION_EAST = {"mikkeli", "savonlinna", "pieksämäki", "kuopio", "iisalmi", "varkaus", "siilinjärvi", "joensuu", "lieksa", "kitee", "outokumpu", "nurmes"}
REGION_NORTH = {"oulu", "raahe", "kempele", "kajaani", "kuhmo", "sotkamo", "rovaniemi", "kemi", "tornio", "kemijärvi", "sodankylä", "inari", "kittilä"}


@dataclass(frozen=True)
class ParamSet:
    valid_from: str
    rate: float                                   # R_CALC_FORMULA
    rate_aland: float
    deductible_share: float                       # R_CALC_BASIC_DEDUCTIBLE
    deductible_base: int
    deductible_per_adult: int
    deductible_per_child: int
    deductible_share_aland: float
    deductible_base_aland: int
    deductible_per_adult_aland: int
    deductible_per_child_aland: int
    min_deductible: float                         # below this the deductible is disregarded (Act § 16)
    min_payment: float                            # R_CALC_MIN_PAYMENT
    max_costs: dict[int, list[int]]               # group -> [1p, 2p, 3p, 4p, per extra]   R_CALC_MAX_COSTS
    max_costs_aland: list[int]
    water_per_person: int                         # R_CALC_WATER_HEATING_FLAT
    heating: dict[str, tuple[int, int]]           # region -> (first person, each additional)
    asset_threshold_one_adult: int                # R_CALC_ASSETS_AS_INCOME
    asset_threshold_two_adults: int
    asset_income_share: float
    asset_deposit_reserve: int
    asset_ceiling: int                            # R_ELIG_ASSET_LIMIT: no allowance at or above
    interest_dividend_threshold: float            # R_CALC_INTEREST_DIVIDEND_THRESHOLD
    earned_income_deduction: float                # R_CALC_EARNED_INCOME_DEDUCTION (0 = abolished)
    students_excluded_by_default: bool            # kela.fi: "If you study, you cannot, as a rule, get general housing allowance"
    owner_occupied_covered: bool                  # kela.fi: "General housing allowance is not available for owner-occupied homes."
    approximate: bool = False                     # True when amounts are at a statutory index level, not the year's indexed values
    sources: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


PARAMS_2026 = ParamSet(
    valid_from="2025-08-01",
    rate=0.70, rate_aland=0.80,
    deductible_share=0.5, deductible_base=667, deductible_per_adult=94, deductible_per_child=296,
    deductible_share_aland=0.42, deductible_base_aland=667, deductible_per_adult_aland=111, deductible_per_child_aland=246,
    min_deductible=10.0, min_payment=15.0,
    max_costs={1: [563, 808, 1019, 1188, 148], 3: [447, 652, 828, 981, 134], 4: [394, 574, 734, 875, 129]},
    max_costs_aland=[470, 687, 871, 1032, 141],
    water_per_person=20,
    heating={"default": (46, 16), "east": (48, 17), "north": (50, 17)},
    asset_threshold_one_adult=10_000, asset_threshold_two_adults=20_000, asset_income_share=0.20,
    asset_deposit_reserve=2_000, asset_ceiling=50_000,
    interest_dividend_threshold=12.02,
    earned_income_deduction=0.0,
    students_excluded_by_default=True,
    owner_occupied_covered=False,
    sources={
        "rate": f"{KELA_INCOME_PAGE}: 'General housing allowance covers a maximum of 70% of your acceptable housing costs. The amount of housing allowance is calculated as follows: 0.7 x (acceptable housing costs – basic deductible).'",
        "rate_aland": f"{KELA_INCOME_PAGE}: 'In the Åland Islands, housing allowance covers a maximum of 80% ... 0.8 x (acceptable housing costs – basic deductible).'",
        "deductible": f"{KELA_INCOME_PAGE}#calculation-formula-for-the-basic-deductible: 'Basic deductible = 0.5 x [T – (667 + 94 x A + 296 x L)]'",
        "deductible_aland": f"{KELA_INCOME_PAGE}: '0.42 x [T - (667 + 111 x A + 246 x L)]'",
        "min_payment": f"{KELA_MAIN_PAGE}: 'If your housing allowance is less than EUR 15 per month, it is not paid out.'",
        "max_costs": f"{KELA_INCOME_PAGE}#the-maximum-limits-for-housing-costs-in-each-municipality: '1 person, a maximum of EUR 563 per month ... + EUR 148 per month for each additional person' (Espoo, Helsinki, Kauniainen and Vantaa); 447/652/828/981/+134 (Hyvinkää ... Vihti); 394/574/734/875/+129 (Other municipalities); 470/687/871/1,032/+141 (Åland)",
        "water_heating": f"{KELA_INCOME_PAGE}: 'Up to EUR 20 per person and per month is accepted.' 'For one-person households, the amount of heating charges accepted is EUR 46 per month ... EUR 16 per month is added for each additional person.' East: 48 + 17; North: 50 + 17",
        "assets": f"{KELA_INCOME_PAGE}#how-your-assets-affect-the-housing-allowance: '... one adult and you have assets of more than EUR 10,000 ... two or more adults ... more than EUR 20,000 ... we will take 20% of the excess into account as income. If your household has assets of EUR 50,000 or more, no housing allowance is paid at all. ... a deduction of EUR 2,000 for disposable income is made from account deposits ... personal'",
        "interest_dividend": f"{KELA_INCOME_PAGE}: 'interest and dividend income ... if it exceeds EUR 12.02 per month.'",
        "students": f"{KELA_MAIN_PAGE}: 'If you study, you cannot, as a rule, get general housing allowance. The majority of students can get the housing supplement for students'",
        "owner_occupied": f"{KELA_INCOME_PAGE}: 'General housing allowance is not available for owner-occupied homes.'",
        "min_deductible": "Act 938/2014 § 16 (consolidated text in corpus): a basic deductible under 10 euros is not taken into account",
    },
    notes=[
        "Act text (2010 index level) gives rate 0.80 and deductible 0.42 x [T - (555 + 92A + 205L)]; the map recorded the version conflict (R_CALC_FORMULA). Kela guidance governs here.",
        "Earned income deduction of 300 EUR (R_CALC_EARNED_INCOME_DEDUCTION) no longer appears on kela.fi; set to 0. Replay cases dated before 2024-04-01 should use an earlier parameter set, which is not yet encoded.",
        "The map lists four Act municipality groups; kela.fi now publishes three mainland tables plus Åland. Groups I and II are merged in this set.",
        "Students were moved to the study grant housing supplement; the map (built from pre-change documents) still treats students as eligible. This is the first divergence the twin surfaced from the map.",
    ],
)

PARAMS_ACT_2015 = ParamSet(
    valid_from="2015-01-01",
    rate=0.80, rate_aland=0.80,
    deductible_share=0.42, deductible_base=555, deductible_per_adult=92, deductible_per_child=205,
    deductible_share_aland=0.42, deductible_base_aland=555, deductible_per_adult_aland=92, deductible_per_child_aland=205,
    min_deductible=10.0, min_payment=15.0,
    max_costs={1: [508, 735, 937, 1095, 137], 2: [492, 706, 890, 1038, 130], 3: [390, 570, 723, 856, 117], 4: [344, 501, 641, 764, 112]},
    max_costs_aland=[344, 501, 641, 764, 112],
    water_per_person=17,
    heating={"default": (38, 13), "east": (40, 14), "north": (41, 14)},
    asset_threshold_one_adult=10_000, asset_threshold_two_adults=20_000, asset_income_share=0.20,
    asset_deposit_reserve=2_000, asset_ceiling=50_000,
    interest_dividend_threshold=10.0,
    earned_income_deduction=300.0,
    students_excluded_by_default=False,
    owner_occupied_covered=True,
    approximate=True,
    sources={
        "rate": "Act 938/2014 § 8 (corpus law-938-2014.txt): 'oikeus saada asumistukea 80 prosenttia'",
        "deductible": "Act § 16: 'Perusomavastuuosuus on 42 prosenttia ... 555 euroa lisättynä 92 eurolla jokaista ... aikuista ja 205 eurolla jokaista ... lasta kohden. Jos perusomavastuuosuus on vähemmän kuin 10 euroa, sitä ei oteta huomioon.'",
        "max_costs": "Act § 10 table (2015 rent-index level): I 508/735/937/1095 +137; II 492/706/890/1038 +130; III 390/570/723/856 +117; IV 344/501/641/764 +112",
        "earned_income_deduction": "Act § 13: '... vähennetään 300 euroa kuukaudessa'",
        "min_payment": "Act § 19: 'Jos maksettava asumistuen määrä olisi pienempi kuin 15 euroa, tukea ei makseta.'",
        "interest_dividend": "Act § 12: 'ylittävät 10 euroa kuukaudessa'",
    },
    notes=[
        "Statutory base values. In each year Kela applied index-adjusted amounts (National Pension Index for § 16, rent index for § 10 from 2018), which this set does not carry. Amounts computed under it are approximate; decisions (granted or rejected, which ground) are not affected by the index.",
        "The asset rules (10,000 / 20,000 / 50,000, 20 %) took effect 2015 per the map; the 2,000 deposit reserve and the owner-occupied exclusion are later changes carried here as the map records them. Owner-occupier cost computation (§ 9 maintenance and financing costs) is not encoded: such cases raise a question.",
        "Rate 0.80 and deduction 300 were in force until 31 March 2024; from 1 April 2024 the rate is 0.70, the deductible share 0.5 and the deduction abolished. The 2024-04-01 to 2025-07-31 set is not encoded separately; PARAMS_2026 applies from 2025-08-01 (students moved to the study housing supplement on 1 August 2025).",
    ],
)

PARAM_SETS = [PARAMS_ACT_2015, PARAMS_2026]


def params_for(decision_date: str) -> ParamSet:
    """Latest set whose valid_from <= decision_date; the earliest set if the date is before all."""
    chosen = None
    for p in sorted(PARAM_SETS, key=lambda p: p.valid_from):
        if p.valid_from <= decision_date:
            chosen = p
    return chosen or PARAM_SETS[0]
