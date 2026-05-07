from pathlib import Path

from founder_sales_os.config import load_company_profile, load_scoring_rules
from founder_sales_os.ingest import read_sales_calls
from founder_sales_os.reporting import build_call_intelligence


ROOT = Path(__file__).resolve().parents[1]


def test_icp_scoring_boundaries() -> None:
    sales_calls = read_sales_calls(ROOT / "data/sample_sales_calls.csv")
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")

    intelligence = build_call_intelligence(sales_calls, company_profile, scoring_rules)
    strong = intelligence[intelligence["call_id"] == "CALL-001"].iloc[0]
    weak = intelligence[intelligence["call_id"] == "CALL-012"].iloc[0]

    assert strong["icp_fit_score"] >= 75
    assert strong["fit_category"] == "Strong fit"
    assert weak["icp_fit_score"] < 50
    assert weak["fit_category"] == "Weak fit"


def test_score_columns_are_bounded() -> None:
    sales_calls = read_sales_calls(ROOT / "data/sample_sales_calls.csv")
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")
    intelligence = build_call_intelligence(sales_calls, company_profile, scoring_rules)

    for column in ["icp_fit_score", "urgency_score", "budget_score", "deal_rescue_priority_score"]:
        assert intelligence[column].between(0, 100).all()
