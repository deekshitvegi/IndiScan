import pytest
from indiscan import Nutrition, score_product


def test_perfect_product_scores_max():
    r = score_product(Nutrition(100, 0, 0, 0, 50, 15, 8), "whole wheat, oats, almonds, dates, milk", "food")
    assert r.score == 1000 and r.grade == "A"


def test_junk_product_scores_low():
    r = score_product(Nutrition(560, 30, 12, 1.5, 1000, 3, 0.5), "sugar, palm oil, maida, INS 102, INS 211")
    assert r.score < 200 and r.grade == "E"


def test_high_risk_additive_caps_score():
    r = score_product(Nutrition(100, 0, 0, 0, 50, 15, 8), "whole wheat, oats, almonds, dates, milk, INS 123")
    assert r.score <= 599


def test_beverage_thresholds_stricter():
    n = Nutrition(45, 10.5, 0, 0, 10, 0, 0)
    assert score_product(n, "", "beverage").score < score_product(n, "", "food").score


def test_bounds_and_validation():
    assert 0 <= score_product(Nutrition(9999, 999, 99, 99, 9999)).score <= 1000
    with pytest.raises(ValueError):
        score_product(Nutrition(sugar_g=-1))
    with pytest.raises(ValueError):
        score_product(Nutrition(), category="x")


def test_samples_rank_sensibly():
    from indiscan.samples import SAMPLES, score_sample
    s = {k: score_sample(k).score for k in SAMPLES}
    assert all(0 <= v <= 1000 for v in s.values())
    assert s["rolled-oats"] > s["glucose-biscuit"] > s["instant-noodles"]
    assert s["buttermilk"] > s["cola"] and s["buttermilk"] > s["fruit-drink"]
    assert s["roasted-chana"] > s["bhujia-namkeen"]
