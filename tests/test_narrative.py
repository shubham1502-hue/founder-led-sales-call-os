from pathlib import Path

from founder_sales_os.config import load_company_profile, load_scoring_rules
from founder_sales_os.ingest import read_sales_calls
from founder_sales_os.narrative import build_narrative_experiments
from founder_sales_os.reporting import build_call_intelligence, build_objection_bank


ROOT = Path(__file__).resolve().parents[1]


def test_narrative_experiment_generation() -> None:
    sales_calls = read_sales_calls(ROOT / "data/sample_sales_calls.csv")
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")
    intelligence = build_call_intelligence(sales_calls, company_profile, scoring_rules)
    objection_bank = build_objection_bank(intelligence)

    markdown = build_narrative_experiments(intelligence, objection_bank)

    assert "What prospects did not understand" in markdown
    assert "Messaging angles to test" in markdown
    assert "Suggested sales-call discovery questions" in markdown
