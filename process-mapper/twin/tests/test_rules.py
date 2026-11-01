"""Kela's own worked examples, from kela.fi (Oct 2026), as tests of the rules and the runner."""

from twin.params import PARAMS_2026 as P
from twin.rules import gha
from twin.runner import Runner
from twin.synthetic import make_case


def test_turku_couple_example():
    # "Eino and Elisa ... Turku ... total income 1,800 ... housing costs 950 ... maximum 652 ... basic deductible 472.50 ... 0,7 x (652 – 472.50) = 125.65"
    c = make_case("ex-turku", 2, 0, "Turku", 950, [1800, 0])
    assert gha.max_costs(c, P).value == 652
    assert gha.basic_deductible(c, P, 1800).value == 472.50
    run = Runner().run(c)
    assert run.outcome.decision == "granted"
    assert run.outcome.monthly_allowance == 125.65


def test_helsinki_cap_example():
    # "Maija lives alone in a rented apartment in Helsinki. She pays EUR 800 ... Up to EUR 563"
    c = make_case("ex-maija", 1, 0, "Helsinki", 800, [0])
    assert gha.max_costs(c, P).value == 563
    assert gha.accepted_costs(c, P).value == 800
    run = Runner().run(c)
    assert run.outcome.monthly_allowance == round(0.7 * 563, 2)


def test_asset_example():
    # "Pekka lives alone ... investment product valued at EUR 15,000 ... EUR 1,000 per year, or EUR 83.33 per month"
    c = make_case("ex-pekka", 1, 0, "Helsinki", 700, [0])
    c.members[0].assets.other = 15000
    r = gha.asset_income(c, P)
    assert r.value == ("income", 83.33)


def test_asset_ceiling():
    c = make_case("ex-ceiling", 1, 0, "Helsinki", 700, [0], deposits=60000)
    run = Runner().run(c)
    assert run.outcome.decision == "rejected" and "R_ELIG_ASSET_LIMIT" in run.outcome.grounds


def test_income_limit_boundary():
    # one adult in Helsinki: 1,844 is the published limit; 1,845 gives less than 15
    lo = Runner().run(make_case("lim-lo", 1, 0, "Helsinki", 700, [1844]))
    hi = Runner().run(make_case("lim-hi", 1, 0, "Helsinki", 700, [1845]))
    assert lo.outcome.decision == "granted" and hi.outcome.decision == "not_paid"


def test_heating_region():
    c = make_case("heat", 1, 0, "Rovaniemi", 500, [1100], heating=True)
    assert gha.accepted_costs(c, P).value == 550  # 500 + 50 (north)


def test_unknown_rent_becomes_question():
    c = make_case("unk", 1, 0, "Helsinki", 0, [1200])
    c.unknowns = ["costs.rent not stated"]
    run = Runner().run(c)
    assert run.outcome.decision == "question" and run.outcome.open_questions


def test_student_excluded_by_current_guidance():
    c = make_case("stud", 1, 0, "Helsinki", 700, [0])
    c.members[0].excluded_student = True
    run = Runner().run(c)
    assert run.outcome.decision == "rejected" and "R_ELIG_STUDENT" in run.outcome.grounds
