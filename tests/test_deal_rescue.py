from pathlib import Path

from founder_sales_os.config import load_company_profile, load_scoring_rules
from founder_sales_os.deal_rescue import build_deal_rescue_queue
from founder_sales_os.ingest import read_sales_calls
from founder_sales_os.reporting import build_call_intelligence


ROOT = Path(__file__).resolve().parents[1]


def test_deal_rescue_priority_logic() -> None:
    sales_calls = read_sales_calls(ROOT / "data/sample_sales_calls.csv")
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")
    intelligence = build_call_intelligence(sales_calls, company_profile, scoring_rules)

    queue = build_deal_rescue_queue(intelligence, scoring_rules)

    assert not queue.empty
    assert "High" in set(queue["priority"])
    assert "Northstar Ledger" in set(queue["company_name"]) or "Atlas FreightOS" in set(queue["company_name"])


def test_deal_rescue_queue_has_required_columns() -> None:
    sales_calls = read_sales_calls(ROOT / "data/sample_sales_calls.csv")
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")
    intelligence = build_call_intelligence(sales_calls, company_profile, scoring_rules)
    queue = build_deal_rescue_queue(intelligence, scoring_rules)

    assert {
        "task_id",
        "company_name",
        "priority",
        "founder_next_action",
        "suggested_followup_message",
        "expected_leverage",
    }.issubset(queue.columns)
